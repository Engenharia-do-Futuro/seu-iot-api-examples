# JavaScript examples

Requires Node.js 20.6+ (built-in `fetch` and `--env-file`). Each folder is self-contained: copy `.env.example` to `.env`, fill in your API key and run it.

| Example | What it does | Endpoints / transport |
|---|---|---|
| [node-rest](node-rest) | Zero-dependency scripts: `npm run contract` prints your contract scope, `npm run data` reads the latest points of a process. | `GET /external/v1/contract`, `GET /external/v1/processes/{uuid}/data` |
| [node-mqtt-websocket](node-mqtt-websocket) | Receives live readings over MQTT on WebSocket (`wss`) using [mqtt.js](https://github.com/mqttjs/MQTT.js) and prints them in readable form. | `GET /contract`, `POST /mqtt-credentials`, then MQTT over WebSocket |

> The MQTT example calls `POST /external/v1/mqtt-credentials`, which **rotates the MQTT password** on every run.

For a browser example (embeddable widget), see [`../web`](../web). See the [documentation](../../docs/en/index.md) for details.
