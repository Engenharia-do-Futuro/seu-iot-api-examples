# Primeros pasos

1. En el panel de Seu IoT, abre **Configuración del proyecto > Contratos de API**.
2. Crea un contrato: ponle un nombre y elige los **procesos** y **dispositivos** a los que puede acceder. Una lista de dispositivos vacía significa todos los dispositivos del proyecto.
3. Emite la **clave de API** y cópiala de inmediato, incluyendo el prefijo `siot_`. Trátala como una contraseña.
4. Comprueba que funciona:

```bash
curl -H "Authorization: Bearer siot_tu_clave" https://seuiot.com.br:8000/external/v1/contract
```

Un JSON que describa tu contrato indica que todo está listo. A partir de aquí:

- datos históricos: [API REST](rest-api.md)
- datos en vivo: [Tiempo real (MQTT)](realtime-mqtt.md)
- un gráfico en tu sitio: [Widgets](widgets.md)

Editar el alcance del contrato en el panel vale desde la próxima solicitud. Quitar elementos también desconecta a los consumidores MQTT en vivo, que se reconectan con la lista de tópicos más corta. Para recibir por MQTT los elementos recién añadidos, pide una nueva credencial.
