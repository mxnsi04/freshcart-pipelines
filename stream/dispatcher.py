"""
stream/dispatcher.py
---------------------
Part D2 – FreshCart / Rapido-style food-order dispatcher.

Publishes a JSON order message every 2 seconds to a RabbitMQ **topic exchange**
named 'rapido-dispatch'.

Routing key format:  <city>.<zone>.<type>
  city  : bangalore | chennai
  zone  : koramangala | indiranagar | whitefield | tnagar
  type  : ride | food

Usage
-----
  # Local broker (Colab):
  python dispatcher.py

  # Hosted broker (CloudAMQP – set env var):
  AMQP_URL=amqps://user:pass@host/vhost python dispatcher.py
"""

import json
import os
import random
import time
import uuid

import pika

EXCHANGE = "rapido-dispatch"
EXCHANGE_TYPE = "topic"

CITIES = ["bangalore", "chennai"]
ZONES = {
    "bangalore": ["koramangala", "indiranagar", "whitefield"],
    "chennai": ["tnagar", "mylapore", "anna_nagar"],
}
TYPES = ["ride", "food"]

AMQP_URL = os.environ.get("AMQP_URL", "amqp://guest:guest@localhost/")


def get_connection():
    params = pika.URLParameters(AMQP_URL)
    return pika.BlockingConnection(params)


def build_message(seq: int) -> tuple[str, dict]:
    """Return (routing_key, message_dict)."""
    city = random.choice(CITIES)
    zone = random.choice(ZONES[city])
    order_type = random.choice(TYPES)
    routing_key = f"{city}.{zone}.{order_type}"

    # Every 10th message is intentionally 'bad' (missing zone field) for Part D3.
    if seq % 10 == 0:
        msg = {
            "id": str(uuid.uuid4()),
            "city": city,
            # "zone": zone,   ← deliberately omitted for NACK demo
            "type": order_type,
            "ts": time.time(),
            "_bad": True,
        }
    else:
        msg = {
            "id": str(uuid.uuid4()),
            "city": city,
            "zone": zone,
            "type": order_type,
            "ts": time.time(),
        }

    return routing_key, msg


def main():
    conn = get_connection()
    channel = conn.channel()

    channel.exchange_declare(exchange=EXCHANGE, exchange_type=EXCHANGE_TYPE, durable=True)

    seq = 0
    print(f"[dispatcher] Publishing to exchange '{EXCHANGE}'. Press Ctrl+C to stop.\n")

    try:
        while True:
            seq += 1
            routing_key, msg = build_message(seq)
            body = json.dumps(msg)

            channel.basic_publish(
                exchange=EXCHANGE,
                routing_key=routing_key,
                body=body,
                properties=pika.BasicProperties(delivery_mode=2),  # persistent
            )

            tag = " *** BAD (no zone) ***" if msg.get("_bad") else ""
            print(f"[{seq:04d}] key={routing_key:<35} id={msg['id'][:8]}{tag}")
            time.sleep(2)

    except KeyboardInterrupt:
        print("\n[dispatcher] Stopped.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
