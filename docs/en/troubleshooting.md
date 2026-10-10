# Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `401` on any call | Key missing, mistyped, revoked or expired | Check the `Authorization: Bearer siot_...` header and the contract status in the dashboard |
| `400` "API key must be sent via the Authorization header" | Key sent in the query string | Move it to the header |
| `404` on `/processes/{uuid}/data` | Process or device not in scope | List the scope with `GET /contract` and edit the contract if needed |
| `429` | More than 60 requests per minute for the contract | Back off and retry; prefer MQTT for live data instead of polling |
| MQTT disconnects right after subscribing | Subscribed to a topic that is not in the returned list | Subscribe only to `topics` from the latest credential |
| MQTT authentication fails after it worked | Another `POST /mqtt-credentials` rotated the password | Use the credential from the most recent call; do not run two clients on one contract with separate handshakes |
| Widget shows an error | Token invalid, revoked or expired | Regenerate the token; see [Widgets](widgets.md) |
| Names show as raw uuids | Process/device was removed from the project | Update the contract scope |
| No values arrive over MQTT | The process does not publish, or the device is offline | Check that the process has `publish_on_execute` enabled and that the device is online |
| MQTT stops and a message arrives on `.../revoked` | The contract was revoked or deleted | Stop and do not reconnect; see [Lifecycle](lifecycle.md) |
| MQTT timestamp does not parse as a date | MQTT uses the firmware format `DD.MM.YYYY HH:MM:SS.ffffff` | Convert it to ISO 8601; see [Real-time](realtime-mqtt.md) |
| `401` after about a year | The key (and MQTT login) is valid for 365 days | Issue a new key in the dashboard |
