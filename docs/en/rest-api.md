# REST API

Base URL: your Seu IoT server, e.g. `https://seuiot.com.br:8000`. All routes live under `/external/v1` and require `Authorization: Bearer <API key>`.

## GET /external/v1/contract

Returns the contract that owns the key and its scope, resolved to names.

```bash
curl -H "Authorization: Bearer $SIOT_API_KEY" "$SIOT_API_BASE_URL/external/v1/contract"
```

```json
{
  "uuid": "...",
  "name": "My contract",
  "process_uuids": ["..."],
  "device_uuids": ["..."],
  "processes": [{ "uuid": "...", "name": "Temperature", "unit": "C" }],
  "devices": [{ "uuid": "...", "name": "Greenhouse sensor 1" }],
  "is_active": true,
  "expires_at": "2027-01-01T00:00:00"
}
```

- `device_uuids` empty means **all devices** of the project.
- `unit` is only set for Linearization processes.
- `name` is `null` if the process/device was removed from the project after being added to the scope.

## GET /external/v1/processes/{process_uuid}/data

Historical data of one process.

| Query param | Description |
|---|---|
| `device_uuid` | Only this device (must be in scope) |
| `start`, `end` | Time range, ISO 8601 in UTC, both inclusive |
| `limit` | Max points. Default `500`, maximum `2000` |

```bash
curl -H "Authorization: Bearer $SIOT_API_KEY" \
  "$SIOT_API_BASE_URL/external/v1/processes/$PROCESS_UUID/data?limit=20"
```

```json
[{ "data": "22.4", "timestamp": "2026-09-30T12:00:00", "mode": 0, "device_uuid": "..." }]
```

The most recent `limit` points are returned in **chronological order** (oldest first). Notes:

- `data` is a string; its format depends on the process type.
- `mode` is the numeric id of the process type.
- Every point carries the `device_uuid` it came from, so one call can cover several devices. Without the `device_uuid` parameter you get the devices the contract allows (all of the project's if it lists none).
- For the latest value, use `limit=1`.
- There is no cursor pagination. To go through more than 2000 points, walk the history in time windows with `start` and `end` (both are inclusive, so discard the repeated boundary point).

## POST /external/v1/mqtt-credentials

Issues or rotates the MQTT credential. Returns `201`:

```json
{
  "username": "...",
  "password": "...",
  "host": "mqtt.seuiot.com.br",
  "ws_port": 8084,
  "topics": ["/12/device-uuid/process-uuid/"]
}
```

The password appears **only in this response**. Every call replaces it, so do not call this route from a consumer at startup. See [Real-time](realtime-mqtt.md).

## Limits

- **60 requests per minute** per contract; beyond that the API answers `429`.
- Each authorized request is counted per UTC day in the contract's usage. MQTT traffic is not counted.
- The key is valid for **365 days** from the moment it is issued; after that the API answers `401`.
- Use REST for history and for the first value. To receive new values, do not poll: use [MQTT](realtime-mqtt.md).

## Errors

Errors return JSON with `message`, `status` and `error_code`.

| HTTP | `error_code` | Meaning |
|---|---|---|
| 400 | `API_CONTRACT_UNAUTHORIZED` | API key sent in the query string |
| 401 | `API_CONTRACT_UNAUTHORIZED` | Missing, invalid, revoked or expired key |
| 404 | `EXTERNAL_API_PROCESS_NOT_IN_SCOPE` | Process not in the contract's scope |
| 404 | `EXTERNAL_API_DEVICE_NOT_IN_SCOPE` | Device not in the contract's scope |
| 429 | `API_CONTRACT_RATE_LIMITED` | Too many requests, retry shortly |

Out-of-scope resources return `404`, not `403`, so the API never reveals whether they exist.
