# Authentication

Seu IoT has two kinds of credential. They are not interchangeable.

| | API key | Widget `embed_token` |
|---|---|---|
| Format | `siot_...` | `siotw_...` |
| Used by | your **server** or scripts | a visitor's **browser** |
| Sent as | `Authorization: Bearer <key>` | part of the widget tag |
| Exposes | the whole contract scope | only the signals of one widget |
| Secret? | **Yes** | No, designed to be public |

## Rules for the API key

- Send it **only** in the `Authorization: Bearer` header. Keys in the query string (`api_key`, `token`, `access_token`, `key`) are rejected with `400`.
- Never put it in front-end code, mobile apps or public repositories. Use environment variables (see the `.env.example` in each example).
- A revoked, inactive or expired key returns `401`.
- Requests are rate limited per contract (currently 60 per minute); excess requests return `429`.

## MQTT credentials

`POST /external/v1/mqtt-credentials` exchanges the API key for a broker username/password. **Every call rotates the password**: the previous MQTT credential stops working. See [Real-time](realtime-mqtt.md).
