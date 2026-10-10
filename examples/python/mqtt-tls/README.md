# Python - live data over MQTT + TLS

Does the HTTPS handshake (`GET /contract`, `POST /mqtt-credentials`), then connects to the broker over native MQTT with TLS (`mqtts`, port 8883) and prints every message in readable form:

```
Device Greenhouse sensor 1 published 22.4 C on process Temperature
```

> Each run calls `POST /mqtt-credentials`, which **rotates the password** and invalidates the previous credential.

## Run

```bash
cp .env.example .env    # fill in SIOT_API_BASE_URL and SIOT_API_KEY
pip install -r requirements.txt
python subscribe.py     # Ctrl+C to stop
```

Requires Python 3.10+. The `mqtts` listener may use a self-signed certificate, so this example does not verify it; broker authentication by username/password still applies. See [Real-time MQTT docs](../../../docs/en/realtime-mqtt.md).
