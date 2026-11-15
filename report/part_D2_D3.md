# Part D2 & D3: RabbitMQ Dispatcher, Drivers, ACK and NACK Implementation

**Date:** 2026-11-15  
**Course:** Data Engineering · Pipeline Orchestration  
**Topic Exchange:** `rapido-dispatch`

---

## 1. System Architecture

```
                       ┌──► [Private Queue: Ravi]    (bangalore.koramangala.*)
                       │
[stream/dispatcher.py] ──► [rapido-dispatch] ──► [Private Queue: Priya]   (bangalore.indiranagar.*)
  (emits every 2s,     │    (Topic Exchange) ──► [Private Queue: Arjun]   (bangalore.*.ride)
   1 in 10 malformed)  │                     ──► [Private Queue: Meena]   (bangalore.*.food)
                       │                     ──► [Private Queue: Karthik] (chennai.tnagar.food)
                       └──► [Private Queue: Control] (bangalore.#)
```

### Components
1. **Exchange:** `rapido-dispatch` (AMQP Type: `topic`, `durable=True`).
2. **Dispatcher (`stream/dispatcher.py`):**
   - Every 2 seconds, selects a city (`bangalore`, `chennai`), a valid zone, and an order type (`ride`, `food`).
   - Emits a JSON payload with fields `id`, `city`, `zone`, `type`, `ts`.
   - Injects a malformed message missing the `zone` field once every 10 messages (for Part D3 evaluation).
3. **Driver Worker (`stream/driver.py NAME PATTERN`):**
   - Creates a private, server-named, exclusive queue (`exclusive=True`).
   - Binds the queue to `rapido-dispatch` with the specified binding pattern.
   - Evaluates incoming payloads:
     - If `zone` is present: logs success and issues `basic_ack`.
     - If `zone` is missing: logs warning and issues `basic_nack(requeue=False)`.

---

## 2. Answers to Core Message Reliability Questions

### Question 1: What happens if a driver crashes before sending an ACK?

In RabbitMQ AMQP messaging with explicit acknowledgements (`auto_ack=False`):
- When a message is delivered to a consumer, RabbitMQ marks the message as `unacked` and retains it in memory.
- If the consumer process crashes, the host machine restarts, or the TCP network connection drops before `basic_ack` is received:
  1. RabbitMQ detects the closure of the AMQP channel / connection.
  2. RabbitMQ transitions the message from `unacked` back to the `ready` state at the head of the queue.
  3. The message is redelivered to the next available consumer subscribed to that queue (or re-delivered when the crashed worker reconnects).
- **Core Benefit:** Guarantees **at-least-once delivery** semantics. No tasks, rides, or food orders are lost due to transient worker crashes.

### Question 2: What would happen if `requeue=True` is used for a message that is always invalid (poison pill)?

- If a driver rejects an inherently invalid message (e.g. malformed JSON or permanently missing mandatory schema field `zone`) with `basic_nack(requeue=True)`:
  1. The broker immediately puts the bad message back onto the queue.
  2. The queue immediately re-dispatches the exact same bad message back to the driver.
  3. The driver fails validation again and issues another `basic_nack(requeue=True)`.
- **System Impact (Poison-Pill Death Spiral):**
  - Causes an **infinite retry loop**, pegging CPU utilization at 100%.
  - Driver logs are flooded with endless identical failure messages.
  - All legitimate, valid orders queued behind the poison message are completely blocked and starved of processing.
- **Best Practice Solution:**
  - Reject permanent validation failures using `basic_nack(requeue=False)`.
  - Discard the message or route it to a **Dead Letter Exchange (DLX)** for inspection by support engineers.
  - Reserve `requeue=True` strictly for temporary, recoverable system errors (such as database deadlocks or network glitches).

---

## 3. D2 & D3 Execution Protocol

### Running the 2-Minute Demonstration
The demonstration runs simultaneously across 4 terminal sessions:
1. **Driver 1 (Ravi):** `python stream/driver.py Ravi "bangalore.koramangala.*"`
2. **Driver 2 (Arjun):** `python stream/driver.py Arjun "bangalore.*.ride"`
3. **Driver 3 (Control):** `python stream/driver.py Control "bangalore.#"`
4. **Dispatcher:** `python stream/dispatcher.py`

### Expected Verification Metrics
- Routing key matches observed in console output exactly correspond to D1 paper predictions.
- Every 10th message (`seq % 10 == 0`) displays:
  - Dispatcher: `*** BAD (no zone) ***`
  - Drivers: `✗ Bad message (no 'zone') – NACK (discard)`
- Valid messages display:
  - Drivers: `✓ ACK | key=...`
