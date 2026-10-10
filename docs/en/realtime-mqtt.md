# Real-time data (MQTT)

Live values are delivered through an MQTT broker. The flow has three steps, implemented in [`examples/python/mqtt-tls`](../../examples/python/mqtt-tls), [`examples/python/mqtt-websocket`](../../examples/python/mqtt-websocket) and [`examples/javascript/node-mqtt-websocket`](../../examples/javascript/node-mqtt-websocket):

1. `GET /external/v1/contract` to learn names and units.
2. `POST /external/v1/mqtt-credentials` to get `username`, `password`, `host`, `ws_port` and `topics`.
3. Connect and subscribe to **every** topic returned.

## Topics and payload

Topic: `/{project_id}/{device_uuid}/{process_uuid}/`

When the contract lists no devices, the device level of the topic is `+`: you receive every device of the project for that process, and the device is identified by the topic.

Payload: JSON text, e.g. `{"answer_type": 1, "data": 22.4, "mode": 3, "id": 7, "timestamp": "31.01.2026 14:05:09.123456"}`. Use the contract scope to turn the uuids into names.

| Field | Meaning |
|---|---|
| `answer_type` | `1` = a reading (what you want). `0` = the device confirming a configuration: ignore it |
| `data` | The value. String, number or boolean depending on the process type |
| `mode` | Numeric id of the process type |
| `id` | Revision of the process that produced the value |
| `timestamp` | Device time in UTC, in the firmware format `DD.MM.YYYY HH:MM:SS.microseconds`. **Not ISO 8601** |

REST returns ISO 8601 timestamps and MQTT does not, so normalize before mixing the two. Conversion example: `31.01.2026 14:05:09.123456` becomes `2026-01-31T14:05:09.123456Z`.

## Transports

| Transport | Port | Certificate | Note |
|---|---|---|---|
| MQTT over WebSocket (`wss`) | `ws_port` from the credentials response (8084 in production), path `/mqtt` | public CA | Default, recommended |
| MQTT over TLS (`mqtts`) | 8883 | may be self-signed | Not in the credentials response |

## Rules

- Each `POST /mqtt-credentials` **rotates the password**. Only request a new credential when you need a new session or after an authentication failure.
- The credential is **subscribe-only** and restricted to the returned topics. Subscribing to any other topic makes the broker **disconnect** the session.
- After you change the contract scope, request a new credential to get the updated topic list.
- Use a random `clientId` (or add a random suffix). Two consumers with the same `clientId` kick each other off the broker.
- Subscribe inside the client's `connect` event, so the subscription is restored after every reconnect.
- You do **not** receive the last value when you subscribe. Fetch the current value once with REST (`limit=1`), then rely on MQTT.
- After being offline, call REST **once** with `start=<last timestamp you processed>` to fill the gap, then go back to MQTT. Never run that call on a timer.
- If nothing arrives, check that the process has `publish_on_execute` enabled and that the device is online.

## Revocation

The topic `/broker/api-contract/<contract_uuid>/revoked` is always granted. A message there means the contract was revoked or deleted: close the client and **do not reconnect**. See [Lifecycle](lifecycle.md).
