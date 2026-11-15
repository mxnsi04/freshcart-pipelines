"""
stream/driver.py
-----------------
Part D2 & D3 – RabbitMQ topic-exchange consumer (driver).

Declares a private, exclusive queue and binds it to 'rapido-dispatch'
using the PATTERN supplied on the command line.

ACK / NACK logic (Part D3):
  - If the message body is missing the 'zone' field → basic_nack(requeue=False)
    (the message is discarded / dead-lettered).
  - Otherwise → basic_ack (message is consumed successfully).

Usage
-----
  python driver.py Ravi  "bangalore.koramangala.*"
  python driver.py Priya "bangalore.indiranagar.*"
  python driver.py Arjun "bangalore.*.ride"
  python driver.py Meena "bangalore.*.food"
  python driver.py Karthik "chennai.tnagar.food"
  python driver.py Control "bangalore.#"

  # Hosted broker:
  AMQP_URL=amqps://user:pass@host/vhost python driver.py Ravi "bangalore.koramangala.*"
"""

import json
import os
import sys

import pika

EXCHANGE = "rapido-dispatch"
EXCHANGE_TYPE = "topic"
AMQP_URL = os.environ.get("AMQP_URL", "amqp://guest:guest@localhost/")


def on_message(channel, method, properties, body, driver_name: str):
    """Callback: ACK valid messages; NACK bad ones (missing zone)."""
    try:
        msg = json.loads(body)
    except json.JSONDecodeError:
        print(f"[{driver_name}] ✗ Could not parse JSON – NACK (discard)")
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        return

    if "zone" not in msg:
        print(
            f"[{driver_name}] ✗ Bad message (no 'zone') – NACK (discard) | id={msg.get('id', '?')[:8]}"
        )
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        return

    print(
        f"[{driver_name}] ✓ ACK | key={method.routing_key:<35} "
        f"city={msg['city']} zone={msg['zone']} type={msg['type']} id={msg['id'][:8]}"
    )
    channel.basic_ack(delivery_tag=method.delivery_tag)


def main():
    if len(sys.argv) != 3:
        print("Usage: python driver.py <NAME> <PATTERN>")
        print('  e.g. python driver.py Ravi "bangalore.koramangala.*"')
        sys.exit(1)

    driver_name = sys.argv[1]
    pattern = sys.argv[2]

    params = pika.URLParameters(AMQP_URL)
    conn = pika.BlockingConnection(params)
    channel = conn.channel()

    channel.exchange_declare(exchange=EXCHANGE, exchange_type=EXCHANGE_TYPE, durable=True)

    # Declare a private, exclusive queue for this driver.
    result = channel.queue_declare(queue="", exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange=EXCHANGE, queue=queue_name, routing_key=pattern)
    channel.basic_qos(prefetch_count=1)

    print(f"[{driver_name}] Listening on pattern '{pattern}' (queue={queue_name})")
    print(f"[{driver_name}] Press Ctrl+C to stop.\n")

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=lambda ch, method, props, body: on_message(
            ch, method, props, body, driver_name
        ),
    )

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
        print(f"\n[{driver_name}] Stopped.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
