# Datos en tiempo real (MQTT)

Los valores en vivo se entregan mediante un broker MQTT. El flujo tiene tres pasos, implementados en [`examples/python/mqtt-tls`](../../examples/python/mqtt-tls), [`examples/python/mqtt-websocket`](../../examples/python/mqtt-websocket) y [`examples/javascript/node-mqtt-websocket`](../../examples/javascript/node-mqtt-websocket):

1. `GET /external/v1/contract` para obtener nombres y unidades.
2. `POST /external/v1/mqtt-credentials` para obtener `username`, `password`, `host`, `ws_port` y `topics`.
3. Conectar y suscribirse a **todos** los tópicos devueltos.

## Tópicos y payload

Tópico: `/{project_id}/{device_uuid}/{process_uuid}/`

Cuando el contrato no lista dispositivos, el nivel del dispositivo en el tópico es `+`: recibes todos los dispositivos del proyecto para ese proceso, y el dispositivo se identifica por el tópico.

Payload: texto JSON, p. ej. `{"answer_type": 1, "data": 22.4, "mode": 3, "id": 7, "timestamp": "31.01.2026 14:05:09.123456"}`. Usa el alcance del contrato para convertir los uuids en nombres.

| Campo | Significado |
|---|---|
| `answer_type` | `1` = una lectura (lo que quieres). `0` = el dispositivo confirmando una configuración: ignórala |
| `data` | El valor. Cadena, número o booleano según el tipo de proceso |
| `mode` | Id numérico del tipo de proceso |
| `id` | Revisión del proceso que produjo el valor |
| `timestamp` | Hora del dispositivo en UTC, en el formato del firmware `DD.MM.YYYY HH:MM:SS.microsegundos`. **No es ISO 8601** |

La REST devuelve timestamps ISO 8601 y el MQTT no, así que normaliza antes de mezclar los dos. Ejemplo de conversión: `31.01.2026 14:05:09.123456` pasa a `2026-01-31T14:05:09.123456Z`.

## Transportes

| Transporte | Puerto | Certificado | Nota |
|---|---|---|---|
| MQTT sobre WebSocket (`wss`) | `ws_port` de la respuesta de credenciales (8084 en producción), ruta `/mqtt` | CA pública | Por defecto, recomendado |
| MQTT sobre TLS (`mqtts`) | 8883 | puede ser autofirmado | No viene en la respuesta de credenciales |

## Reglas

- Cada `POST /mqtt-credentials` **rota la contraseña**. Pide una nueva credencial solo cuando necesites una nueva sesión o tras un fallo de autenticación.
- La credencial es **solo de suscripción** y está restringida a los tópicos devueltos. Suscribirse a cualquier otro tópico hace que el broker **desconecte** la sesión.
- Después de cambiar el alcance del contrato, pide una nueva credencial para obtener la lista de tópicos actualizada.
- Usa un `clientId` aleatorio (o añade un sufijo aleatorio). Dos consumidores con el mismo `clientId` se expulsan entre sí del broker.
- Suscríbete dentro del evento `connect` del cliente, para que la suscripción se restaure en cada reconexión.
- **No** recibes el último valor al suscribirte. Obtén el valor actual una vez por REST (`limit=1`) y luego confía en el MQTT.
- Tras estar sin conexión, llama a la REST **una vez** con `start=<último timestamp procesado>` para rellenar el hueco y vuelve al MQTT. Nunca ejecutes esa llamada en un temporizador.
- Si no llega nada, revisa que el proceso tenga `publish_on_execute` habilitado y que el dispositivo esté en línea.

## Revocación

El tópico `/broker/api-contract/<contract_uuid>/revoked` siempre está permitido. Un mensaje ahí significa que el contrato fue revocado o eliminado: cierra el cliente y **no vuelvas a conectar**. Mira [Ciclo de vida](lifecycle.md).
