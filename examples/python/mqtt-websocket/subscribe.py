"""Seu IoT example: HTTPS handshake + live subscription over MQTT on WebSocket (ws/wss).

Same flow as ../mqtt-tls (same handshake, same password rotation on every
call, same name/unit lookup via GET /external/v1/contract); only the transport
changes: WebSocket instead of native MQTT.

The broker serves wss (port 8084) with a public-CA certificate, which is what
the credentials response returns in `ws_port`.
"""

import json
import os
import ssl
import sys
from datetime import datetime, timezone

import paho.mqtt.client as mqtt
import requests
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.environ["SIOT_API_BASE_URL"].rstrip("/")
API_KEY = os.environ["SIOT_API_KEY"]
WS_TLS = os.getenv("SIOT_WS_TLS", "true").lower() == "true"
VERIFY_TLS = os.getenv("SIOT_VERIFY_TLS", "true").lower() == "true"

AUTH_HEADERS = {"Authorization": f"Bearer {API_KEY}"}


def fetch_contract_scope() -> tuple[dict, dict]:
    response = requests.get(
        f"{API_BASE_URL}/external/v1/contract", headers=AUTH_HEADERS, verify=VERIFY_TLS, timeout=10
    )
    response.raise_for_status()
    contract = response.json()
    return (
        {p["uuid"]: p for p in contract["processes"]},
        {d["uuid"]: d for d in contract["devices"]},
    )


def issue_mqtt_credentials() -> dict:
    response = requests.post(
        f"{API_BASE_URL}/external/v1/mqtt-credentials", headers=AUTH_HEADERS, verify=VERIFY_TLS, timeout=10
    )
    response.raise_for_status()
    return response.json()


def device_time(payload_json: dict) -> str:
    """The firmware sends "timestamp" as "DD.MM.YYYY HH:MM:SS.microseconds" in UTC
    (not ISO 8601). Returns it as ISO 8601 UTC, or the raw value if it does not match."""
    raw = payload_json.get("timestamp") if isinstance(payload_json, dict) else None
    if not raw:
        return "unknown"
    try:
        parsed = datetime.strptime(raw, "%d.%m.%Y %H:%M:%S.%f").replace(tzinfo=timezone.utc)
    except ValueError:
        return str(raw)
    return parsed.isoformat(timespec="milliseconds")


def describe_message(topic: str, payload: bytes, processes_by_uuid: dict, devices_by_uuid: dict, received_at: str) -> str:
    """Topic format: /{project_id}/{device_uuid}/{process_uuid}/ - payload is JSON with a "data" field.
    Falls back to the raw uuid if the device/process no longer exists in the project."""
    parts = topic.strip("/").split("/")
    if len(parts) != 3:
        return f"[{topic}] {payload.decode('utf-8', errors='replace')}"

    _project_id, device_uuid, process_uuid = parts
    device = devices_by_uuid.get(device_uuid) or {}
    process = processes_by_uuid.get(process_uuid) or {}
    device_name = device.get("name") or device_uuid
    process_name = process.get("name") or process_uuid
    unit = process.get("unit")

    try:
        body = json.loads(payload.decode("utf-8"))
        value = body.get("data")
    except (json.JSONDecodeError, UnicodeDecodeError):
        body = {}
        value = payload.decode("utf-8", errors="replace")

    unit_suffix = f" {unit}" if unit else ""
    return (
        f"[data time {device_time(body)} | received {received_at}] "
        f"Device {device_name} published {value}{unit_suffix} on process {process_name}"
    )


def on_connect(client, userdata, flags, rc):
    if rc != 0:
        print(f"[websocket] connection failed (rc={rc})")
        return
    topics = userdata["topics"]
    print(f"[websocket] connected - subscribing to {len(topics)} topic(s):")
    for topic in topics:
        print(f"  - {topic}")
        client.subscribe(topic)


def on_message(client, userdata, message):
    received_at = datetime.now(timezone.utc).isoformat(timespec="milliseconds")
    print(
        describe_message(
            message.topic, message.payload, userdata["processes_by_uuid"], userdata["devices_by_uuid"], received_at
        )
    )


def on_disconnect(client, userdata, rc):
    print(f"[websocket] disconnected (rc={rc})")


def main() -> None:
    processes_by_uuid, devices_by_uuid = fetch_contract_scope()
    print(f"[websocket] contract scope: {len(processes_by_uuid)} process(es), {len(devices_by_uuid)} device(s)")

    credentials = issue_mqtt_credentials()
    print(f"[websocket] credential issued - username={credentials['username']}")

    client = mqtt.Client(
        userdata={
            "topics": credentials["topics"],
            "processes_by_uuid": processes_by_uuid,
            "devices_by_uuid": devices_by_uuid,
        },
        transport="websockets",
    )
    client.username_pw_set(credentials["username"], credentials["password"])
    client.ws_set_options(path="/mqtt")

    scheme = "ws"
    if WS_TLS:
        scheme = "wss"
        if VERIFY_TLS:
            client.tls_set()
        else:
            client.tls_set(cert_reqs=ssl.CERT_NONE)
            client.tls_insecure_set(True)

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    print(f"[websocket] connecting to {scheme}://{credentials['host']}:{credentials['ws_port']}/mqtt ...")
    client.connect(credentials["host"], credentials["ws_port"], keepalive=30)

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n[websocket] shutting down...")
        client.disconnect()


if __name__ == "__main__":
    sys.exit(main())
