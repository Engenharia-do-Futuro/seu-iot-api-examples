# Widgets incrustables

Un widget es un gráfico que pegas en cualquier página web con una etiqueta `<script>`. Ejemplo: [`examples/web/widget-embed`](../../examples/web/widget-embed).

## Crear el widget

1. Panel > Configuración del proyecto > Contratos de API > tu contrato > pestaña **Widgets**.
2. Crea un widget para una de las señales del alcance del contrato.
3. Haz clic en el icono de código (`</>`), genera el `embed_token` y copia la etiqueta.

## Incrustar

```html
<script src="https://seuiot.com.br:8000/widgets/v1/embed.js"
        data-widget="siotw_..." async></script>
```

El script inserta un `<iframe>` justo después de sí mismo, aislado del CSS y JavaScript de tu página, y lo redimensiona según su contenido. Un token inválido, revocado o expirado muestra un error visible en lugar de un área en blanco.

## Tema

- Por defecto: sigue la preferencia del sistema/navegador del visitante (`prefers-color-scheme`).
- `data-theme="light"` o `"dark"` en el `<script>` fuerza un tema inicial.
- Cambio en vivo desde tu página, sin recargar:

```js
window.SeuIoTWidget.setTheme("siotw_...", "dark"); // o "light"
```

`embed.js` se carga con `async`; las llamadas hechas antes de que termine de cargar se ignoran.

## Notas de seguridad

- El `embed_token` es público por diseño y solo expone las señales de ese widget. Nunca es tu clave de API.
- `/widgets/v1/embed.js` se sirve con CORS abierto a cualquier origen. Todas las demás rutas requieren sesión o clave de API.
- Para que un widget deje de funcionar, revócalo o elimínalo en el panel.

## Límites y ciclo de vida

- Un widget muestra de 1 a 20 dispositivos, todos dentro de los dispositivos del contrato. Con varios, el visitante elige cuál ver.
- Cualquier tipo de gráfico, excepto `table` y `geo_map`. Los colores deben ser hex (`#rrggbb`) o nombre de color, porque el widget se renderiza en una página pública.
- El `embed_token` vale 365 días.
- Revocar el contrato apaga sus widgets, incluso para visitantes que ya están en la página. Reactivar el contrato **no** los vuelve a encender: el dueño revisa y reactiva cada uno.
- No refresques la página con un temporizador ni llames a las rutas públicas `/bootstrap` y `/data` del widget desde tu código: el widget ya se actualiza solo por MQTT, `/bootstrap` reemplaza la contraseña MQTT del widget para todos los visitantes, y cada carga cuenta en el uso del contrato.
