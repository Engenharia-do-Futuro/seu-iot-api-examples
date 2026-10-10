# Node.js - live data over MQTT on WebSocket

Handshake over HTTPS, then a live subscription with [mqtt.js](https://github.com/mqttjs/MQTT.js) over `wss`. Node 20.6+.

> Each run **rotates the MQTT password** (`POST /external/v1/mqtt-credentials`).

```bash
cp .env.example .env    # fill in SIOT_API_BASE_URL and SIOT_API_KEY
npm install
npm start               # Ctrl+C to stop
```

See [Real-time MQTT docs](../../../docs/en/realtime-mqtt.md).
