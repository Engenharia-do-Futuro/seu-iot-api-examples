# Lifecycle: expiry, rotation, revocation and usage

## Expiry

The API key, and the MQTT login that comes with it, are valid for **365 days**. After that, REST answers `401` and MQTT refuses to connect. Issue a new key in the dashboard. A widget's `embed_token` also lasts 365 days.

## Rotation

Rotation is done in the dashboard. It regenerates the API key **and** the MQTT login together. The previous ones stop working at once, with no overlap, so update your consumer's secrets right after.

Calling `POST /external/v1/mqtt-credentials` (or a widget's public `/bootstrap`) also rotates the MQTT password. Avoid it in running code.

## Revocation

- **Revoking** a contract: REST answers `401` immediately, the MQTT login is disabled, connected consumers receive a message on `/broker/api-contract/<contract_uuid>/revoked` and are disconnected, and its widgets are switched off.
- **Reactivating** brings back the **same** key and MQTT login. Widgets stay off until the owner reactivates each one.
- **Deleting** a contract sends it to the trash: it stops working immediately and is purged later.
- A consumer that receives the revoked message must stop and **not** retry.

## Scope changes

Editing the contract's processes and devices is done in the dashboard. Removing items takes effect on the next REST call and disconnects live MQTT consumers, so they reconnect with the narrower topic list.

## Monitoring usage

The dashboard shows, per contract, the REST requests of today and of the last 30 days, and the widget loads, with a daily series. MQTT is not counted.

If the REST number keeps growing when you expected live updates, a consumer is polling: replace it with an [MQTT](realtime-mqtt.md) subscription.

## Limits of a contract

- It belongs to **one project**. For two projects, create two contracts.
- Name: up to 100 characters.
- Scope: 1 to 50 processes and up to 50 devices. Any listed device may be read for any listed process. With no devices listed, every device of the project is included, even ones added later.
