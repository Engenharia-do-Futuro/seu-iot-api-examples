# Solución de problemas

| Síntoma | Causa probable | Solución |
|---|---|---|
| `401` en cualquier llamada | Clave ausente, mal escrita, revocada o expirada | Revisa la cabecera `Authorization: Bearer siot_...` y el estado del contrato en el panel |
| `400` "API key must be sent via the Authorization header" | Clave enviada en la query string | Muévela a la cabecera |
| `404` en `/processes/{uuid}/data` | Proceso o dispositivo fuera del alcance | Lista el alcance con `GET /contract` y edita el contrato si hace falta |
| `429` | Más de 60 solicitudes por minuto en el contrato | Espera y reintenta; prefiere MQTT para datos en vivo en lugar de polling |
| MQTT se desconecta justo después de suscribirse | Te suscribiste a un tópico que no está en la lista devuelta | Suscríbete solo a los `topics` de la credencial más reciente |
| La autenticación MQTT falla después de haber funcionado | Otro `POST /mqtt-credentials` rotó la contraseña | Usa la credencial de la llamada más reciente; no ejecutes dos clientes en un contrato con handshakes separados |
| El widget muestra un error | Token inválido, revocado o expirado | Genera el token de nuevo; mira [Widgets](widgets.md) |
| Los nombres aparecen como uuids | El proceso/dispositivo se eliminó del proyecto | Actualiza el alcance del contrato |
| No llegan valores por MQTT | El proceso no publica, o el dispositivo está sin conexión | Revisa que el proceso tenga `publish_on_execute` habilitado y que el dispositivo esté en línea |
| El MQTT se detiene y llega un mensaje en `.../revoked` | El contrato fue revocado o eliminado | Detente y no vuelvas a conectar; mira [Ciclo de vida](lifecycle.md) |
| El timestamp del MQTT no se convierte en fecha | El MQTT usa el formato del firmware `DD.MM.YYYY HH:MM:SS.ffffff` | Conviértelo a ISO 8601; mira [Tiempo real](realtime-mqtt.md) |
| `401` después de cerca de un año | La clave (y el login MQTT) vale 365 días | Emite una clave nueva en el panel |
