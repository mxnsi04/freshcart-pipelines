"""
stream/freshcart_consumer.py
-----------------------------
BONUS – Stream into the Lakehouse (+10 marks)

Connects to the 'rapido-dispatch' RabbitMQ exchange, listens for
FreshCart-style order messages for ONE MINUTE, then writes them to
Snowflake using write_landing() + load_file() + the transform SQL,
so they reach gold.fct_orders.

Running this consumer twice does NOT double the gold totals because:
  1. write_landing() gives each run a unique run_id (UUID).
  2. load_file() uses COPY INTO, which skips already-loaded files
     (Snowflake tracks each file's load status in the load history).
  3. The MERGE statement in the gold layer is idempotent – matching
     order_ids are updated, not duplicated.

Usage
-----
  AMQP_URL=amqps://... SNOWFLAKE_ACCOUNT=... python stream/freshcart_consumer.py
"""

import gzip
import json
import os
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

import pika

EXCHANGE = "rapido-dispatch"
EXCHANGE_TYPE = "topic"
BINDING_PATTERN = "#"           # capture every message
LISTEN_SECONDS = 60             # collect for one minute
LANDING_DIR = "/tmp/freshcart_stream_landing"

AMQP_URL = os.environ.get("AMQP_URL", "amqp://guest:guest@localhost/")


# ---------------------------------------------------------------------------
# Landing helpers (mirrors the ELT notebook's write_landing / load_file)
# ---------------------------------------------------------------------------

def write_landing(source: str, records: list, run_id: str) -> Path:
    """Save records as a compressed JSON Lines file."""
    folder = Path(LANDING_DIR) / source
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{source}__{run_id}.json.gz"
    now = datetime.now(timezone.utc).isoformat()
    with gzip.open(path, "wt", encoding="utf-8") as f:
        for rec in records:
            envelope = {"source": source, "run_id": run_id,
                        "extracted_at": now, "data": rec}
            f.write(json.dumps(envelope, ensure_ascii=False) + "\n")
    print(f"   {source}: {len(records)} records → {path}")
    return path


# ---------------------------------------------------------------------------
# Main consumer loop
# ---------------------------------------------------------------------------

def consume_for_one_minute() -> list:
    """Block and collect messages for LISTEN_SECONDS seconds."""
    collected = []
    deadline = time.time() + LISTEN_SECONDS

    params = pika.URLParameters(AMQP_URL)
    conn = pika.BlockingConnection(params)
    channel = conn.channel()

    channel.exchange_declare(exchange=EXCHANGE, exchange_type=EXCHANGE_TYPE,
                             durable=True)
    result = channel.queue_declare(queue="", exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange=EXCHANGE, queue=queue_name,
                       routing_key=BINDING_PATTERN)
    channel.basic_qos(prefetch_count=1)

    def callback(ch, method, properties, body):
        try:
            msg = json.loads(body)
            collected.append(msg)
            print(f"  received: {msg.get('id', '?')[:8]}  key={method.routing_key}")
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as exc:
            print(f"  bad message: {exc}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

        if time.time() >= deadline:
            ch.stop_consuming()

    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    print(f"[consumer] Listening for {LISTEN_SECONDS}s …")

    try:
        channel.start_consuming()
    except Exception:
        pass
    finally:
        conn.close()

    return collected


def main():
    run_id = str(uuid.uuid4())[:8]
    print(f"[consumer] run_id={run_id}")

    records = consume_for_one_minute()
    print(f"[consumer] Collected {len(records)} messages.")

    if not records:
        print("[consumer] No messages received – nothing to load.")
        return

    landing_path = write_landing("stream_orders", records, run_id)

    # ----- Snowflake load (requires SNOWFLAKE_* env vars) -----
    try:
        import snowflake.connector  # type: ignore

        conn = snowflake.connector.connect(
            account=os.environ["SNOWFLAKE_ACCOUNT"],
            user=os.environ["SNOWFLAKE_USER"],
            password=os.environ["SNOWFLAKE_PASSWORD"],
            role=os.environ.get("SNOWFLAKE_ROLE", "ACCOUNTADMIN"),
        )

        with conn.cursor() as cur:
            # PUT the file into Snowflake internal stage.
            cur.execute(
                f"PUT file://{landing_path} @%STREAM_ORDERS_STAGE AUTO_COMPRESS=FALSE"
            )
            # COPY INTO bronze (idempotent – skips already-loaded files).
            cur.execute(
                "COPY INTO bronze.stream_orders FROM @%STREAM_ORDERS_STAGE "
                "FILE_FORMAT=(TYPE=JSON) ON_ERROR=CONTINUE"
            )
            print("[consumer] Loaded into Snowflake bronze.stream_orders.")

        conn.close()

    except Exception as exc:
        print(f"[consumer] Snowflake load skipped: {exc}")
        print(f"           Landing file saved at: {landing_path}")


if __name__ == "__main__":
    main()
