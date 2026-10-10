# Embeddable widgets

A widget is a chart you paste into any web page with one `<script>` tag. Example: [`examples/web/widget-embed`](../../examples/web/widget-embed).

## Create the widget

1. Dashboard > Project settings > API contracts > your contract > **Widgets** tab.
2. Create a widget for one of the signals in the contract's scope.
3. Click the code icon (`</>`), generate the `embed_token` and copy the tag.

## Embed

```html
<script src="https://seuiot.com.br:8000/widgets/v1/embed.js"
        data-widget="siotw_..." async></script>
```

The script inserts an `<iframe>` right after itself, isolated from your page's CSS and JavaScript, and resizes it to its content. An invalid, revoked or expired token shows a visible error instead of a blank area.

## Theme

- Default: follows the visitor's system/browser preference (`prefers-color-scheme`).
- `data-theme="light"` or `"dark"` on the `<script>` forces an initial theme.
- Live switch from your page, without reloading:

```js
window.SeuIoTWidget.setTheme("siotw_...", "dark"); // or "light"
```

`embed.js` loads with `async`; calls made before it finishes loading are ignored.

## Security notes

- The `embed_token` is public by design and only exposes the signals of that widget. It is never your API key.
- `/widgets/v1/embed.js` is served with CORS open to any origin. Every other route requires a session or an API key.
- To stop a widget from working, revoke or delete it in the dashboard.

## Limits and lifecycle

- A widget shows 1 to 20 devices, all inside the contract's devices. With several, the visitor picks which one to see.
- Any chart type except `table` and `geo_map`. Colors must be hex (`#rrggbb`) or a color name, because the widget is rendered on a public page.
- The `embed_token` is valid for 365 days.
- Revoking the contract switches off its widgets, including for visitors already on the page. Reactivating the contract does **not** switch them back on: the owner reviews and reactivates each widget.
- Do not refresh the page on a timer or call the widget's public `/bootstrap` and `/data` routes from your own code: the widget already updates itself over MQTT, `/bootstrap` replaces the widget's MQTT password for every visitor, and every load counts in the contract's usage.
