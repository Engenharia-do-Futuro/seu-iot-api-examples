# seu-iot-api-examples

Official integration examples for the Seu IoT platform: API contracts (HTTPS/MQTT data access) and embeddable widgets, in multiple languages.

🌐 **Seu IoT:** <https://seuiot.com.br>

## About Seu IoT and this repository

[Seu IoT](https://seuiot.com.br) is a platform for connecting IoT devices, collecting their data and monitoring it in dashboards. Inside a Seu IoT project, devices send readings for each *process* (for example, a temperature sensor), and you can view them in the web app.

Sometimes that data needs to leave the platform: feeding your own system, a script, a spreadsheet or your company's website. For that, Seu IoT offers **API contracts**. A contract is a scoped and revocable API key that exposes only the processes and devices you choose, and it can be used to:

- **query** the contract's scope and historical data over HTTPS (REST);
- **receive** readings live over MQTT (native TLS or WebSocket);
- **embed** ready-made charts in any web page with a single `<script>` tag (widgets).

This repository is the companion for that external side of the platform. It documents how each API works and provides small, runnable examples showing how to consume it from your own code. It contains no platform source code: everything here talks to Seu IoT only through its public API.

**Docs:** [English](docs/en/index.md) · [Português](docs/pt-br/index.md) · [Español](docs/es/index.md)

## What do you want to do?

| Goal | Example | Docs |
|---|---|---|
| Check your key and see what it can access | [python/rest-contract](examples/python/rest-contract), [javascript/node-rest](examples/javascript/node-rest) | [REST API](docs/en/rest-api.md) |
| Read historical data | [python/rest-process-data](examples/python/rest-process-data), [javascript/node-rest](examples/javascript/node-rest) | [REST API](docs/en/rest-api.md) |
| Receive data live | [python/mqtt-tls](examples/python/mqtt-tls), [python/mqtt-websocket](examples/python/mqtt-websocket), [javascript/node-mqtt-websocket](examples/javascript/node-mqtt-websocket) | [Real-time](docs/en/realtime-mqtt.md) |
| Embed a chart in a website | [web/widget-embed](examples/web/widget-embed) | [Widgets](docs/en/widgets.md) |

New here? Start with [Getting started](docs/en/getting-started.md).

## Repository layout

```
docs/{en,pt-br,es}/   documentation, one folder per language (same file names)
examples/python/      REST and MQTT examples (Python 3.10+)
examples/javascript/  REST and MQTT examples (Node.js 20.6+)
examples/web/         browser examples (widget embed)
```

Each example is self-contained: its own README, dependencies and `.env.example`. Copy `.env.example` to `.env` and fill in your values. **Never commit your `.env` or your API key.**

## License

[CC0 1.0](LICENSE)
