# Python - live data over MQTT on WebSocket

Same flow as [mqtt-tls](../mqtt-tls), but the broker connection is MQTT over WebSocket (`wss`, host and port come from the credentials response). Use it when raw MQTT ports are blocked in your network.

> Each run **rotates the MQTT password**.

## Run

```bash
cp .env.example .env    # fill in SIOT_API_BASE_URL and SIOT_API_KEY
pip install -r requirements.txt
python subscribe.py     # Ctrl+C to stop
```

