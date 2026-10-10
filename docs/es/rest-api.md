# API REST

URL base: tu servidor Seu IoT, p. ej. `https://seuiot.com.br:8000`. Todas las rutas están bajo `/external/v1` y requieren `Authorization: Bearer <clave de API>`.

## GET /external/v1/contract

Devuelve el contrato dueño de la clave y su alcance, ya resuelto a nombres.

```bash
curl -H "Authorization: Bearer $SIOT_API_KEY" "$SIOT_API_BASE_URL/external/v1/contract"
```

```json
{
  "uuid": "...",
  "name": "Mi contrato",
  "process_uuids": ["..."],
  "device_uuids": ["..."],
  "processes": [{ "uuid": "...", "name": "Temperatura", "unit": "C" }],
  "devices": [{ "uuid": "...", "name": "Sensor del invernadero 1" }],
  "is_active": true,
  "expires_at": "2027-01-01T00:00:00"
}
```

- `device_uuids` vacío significa **todos los dispositivos** del proyecto.
- `unit` solo existe para procesos de tipo Linealización.
- `name` es `null` si el proceso/dispositivo se eliminó del proyecto después de entrar en el alcance.

## GET /external/v1/processes/{process_uuid}/data

Datos históricos de un proceso.

| Parámetro de query | Descripción |
|---|---|
| `device_uuid` | Solo este dispositivo (debe estar en el alcance) |
| `start`, `end` | Rango de tiempo, ISO 8601 en UTC, ambos inclusivos |
| `limit` | Máximo de puntos. Por defecto `500`, máximo `2000` |

```bash
curl -H "Authorization: Bearer $SIOT_API_KEY" \
  "$SIOT_API_BASE_URL/external/v1/processes/$PROCESS_UUID/data?limit=20"
```

```json
[{ "data": "22.4", "timestamp": "2026-09-30T12:00:00", "mode": 0, "device_uuid": "..." }]
```

Los `limit` puntos más recientes se devuelven en **orden cronológico** (del más antiguo al más nuevo). Notas:

- `data` es una cadena; su formato depende del tipo de proceso.
- `mode` es el id numérico del tipo de proceso.
- Cada punto trae el `device_uuid` del que proviene, así que una llamada puede cubrir varios dispositivos. Sin el parámetro `device_uuid` recibes los dispositivos que el contrato permite (todos los del proyecto, si no lista ninguno).
- Para el último valor, usa `limit=1`.
- No hay paginación por cursor. Para recorrer más de 2000 puntos, avanza el historial en ventanas de tiempo con `start` y `end` (ambos son inclusivos, así que descarta el punto repetido en el borde).

## POST /external/v1/mqtt-credentials

Emite o rota la credencial MQTT. Devuelve `201`:

```json
{
  "username": "...",
  "password": "...",
  "host": "mqtt.seuiot.com.br",
  "ws_port": 8084,
  "topics": ["/12/device-uuid/process-uuid/"]
}
```

La contraseña aparece **solo en esta respuesta**. Cada llamada la reemplaza, así que no llames a esta ruta al arrancar un consumidor. Mira [Tiempo real](realtime-mqtt.md).

## Límites

- **60 solicitudes por minuto** por contrato; por encima de eso la API responde `429`.
- Cada solicitud autorizada se cuenta por día UTC en el uso del contrato. El tráfico MQTT no se cuenta.
- La clave vale **365 días** desde su emisión; después la API responde `401`.
- Usa REST para el historial y para el primer valor. Para recibir valores nuevos, no hagas polling: usa [MQTT](realtime-mqtt.md).

## Errores

Los errores devuelven JSON con `message`, `status` y `error_code`.

| HTTP | `error_code` | Significado |
|---|---|---|
| 400 | `API_CONTRACT_UNAUTHORIZED` | Clave de API enviada en la query string |
| 401 | `API_CONTRACT_UNAUTHORIZED` | Clave ausente, inválida, revocada o expirada |
| 404 | `EXTERNAL_API_PROCESS_NOT_IN_SCOPE` | Proceso fuera del alcance del contrato |
| 404 | `EXTERNAL_API_DEVICE_NOT_IN_SCOPE` | Dispositivo fuera del alcance del contrato |
| 429 | `API_CONTRACT_RATE_LIMITED` | Demasiadas solicitudes, reintenta en un momento |

Los recursos fuera del alcance devuelven `404`, no `403`, para que la API nunca revele si existen.
