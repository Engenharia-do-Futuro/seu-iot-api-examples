# Autenticación

Seu IoT tiene dos tipos de credencial, que no son intercambiables.

| | Clave de API | `embed_token` de widget |
|---|---|---|
| Formato | `siot_...` | `siotw_...` |
| Usada por | tu **servidor** o scripts | el **navegador** del visitante |
| Enviada como | `Authorization: Bearer <clave>` | parte de la etiqueta del widget |
| Expone | todo el alcance del contrato | solo las señales de un widget |
| ¿Secreta? | **Sí** | No, diseñada para ser pública |

## Reglas para la clave de API

- Envíala **solo** en la cabecera `Authorization: Bearer`. Las claves en la query string (`api_key`, `token`, `access_token`, `key`) se rechazan con `400`.
- Nunca la pongas en código de front-end, apps móviles ni repositorios públicos. Usa variables de entorno (mira el `.env.example` de cada ejemplo).
- Una clave revocada, inactiva o expirada devuelve `401`.
- Las solicitudes tienen límite de frecuencia por contrato (actualmente 60 por minuto); el exceso devuelve `429`.

## Credenciales MQTT

`POST /external/v1/mqtt-credentials` cambia la clave de API por usuario/contraseña del broker. **Cada llamada rota la contraseña**: la credencial MQTT anterior deja de funcionar. Mira [Tiempo real](realtime-mqtt.md).
