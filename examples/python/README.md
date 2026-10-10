# Python examples

Requires Python 3.10+. Each folder is self-contained (own `requirements.txt` and `.env.example`): copy `.env.example` to `.env`, fill in your API key and run the script.

| Example | What it does | Endpoints / transport |
|---|---|---|
| [rest-contract](rest-contract) | Prints your API contract and the processes/devices in its scope. The simplest way to check that your key works. | `GET /external/v1/contract` |
| [rest-process-data](rest-process-data) | Reads the latest historical points of one process, optionally filtered by device. | `GET /external/v1/processes/{uuid}/data` |
| [mqtt-tls](mqtt-tls) | Receives live readings over native MQTT with TLS (`mqtts`, port 8883) and prints them in readable form. | `GET /contract`, `POST /mqtt-credentials`, then MQTT |
| [mqtt-websocket](mqtt-websocket) | Same as `mqtt-tls`, but over MQTT on WebSocket (`wss`). Useful when raw MQTT ports are blocked. | `GET /contract`, `POST /mqtt-credentials`, then MQTT over WebSocket |

Where to start: run `rest-contract` first, then pick REST for history or MQTT for live data.

> The MQTT examples call `POST /external/v1/mqtt-credentials`, which **rotates the MQTT password** on every run.

See the [documentation](../../docs/en/index.md) for details.
