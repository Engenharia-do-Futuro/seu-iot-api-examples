# Getting started

1. In the Seu IoT dashboard, open **Project settings > API contracts**.
2. Create a contract: give it a name and choose the **processes** and **devices** it can access. An empty device list means every device of the project.
3. Issue the **API key** and copy it right away, including the `siot_` prefix. Treat it like a password.
4. Check that it works:

```bash
curl -H "Authorization: Bearer siot_your_key" https://seuiot.com.br:8000/external/v1/contract
```

A JSON document describing your contract means you are ready. From here:

- historical data: [REST API](rest-api.md)
- live data: [Real-time (MQTT)](realtime-mqtt.md)
- a chart on your site: [Widgets](widgets.md)

Editing the contract scope in the dashboard takes effect on the next request. Removing items also disconnects live MQTT consumers, so they reconnect with the narrower topic list. To receive newly added items over MQTT, request a new credential.

## Visual guide

![Dashboard > Project settings > API contracts: the list of the project's contracts.](../../images/getting-started/01-api-contracts-list.png)

![Creating a contract: name, processes and devices in scope.](../../images/getting-started/02-create-contract.png)

![Issuing the key: the API key and MQTT credentials appear only once (secrets hidden in this picture).](../../images/getting-started/03-issue-key.png)
