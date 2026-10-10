# Conectar una IA (MCP)

Los asistentes de IA como Claude, Cursor o Gemini CLI pueden trabajar con tu cuenta de Seu IoT mediante **MCP** (Model Context Protocol). El asistente es solo una interfaz más de tu cuenta: solo ve los proyectos que liberes, solo hace lo que permitas, y todo lo sensible espera tu aprobación en el panel.

Esto es distinto de los [contratos de API](getting-started.md). Un contrato deja que un *sistema externo* lea datos con una clave de API. MCP deja que un *asistente de IA* trabaje dentro de tu cuenta (listar proyectos, leer datos, crear procesos y gráficos, incluso pedir un contrato). Un asistente también puede crear contratos por ti, con tu aprobación.

## No hay nada que habilitar

No existe un interruptor para activar. La conexión solo existe cuando **autorizas una app**, y puedes revocarla en cualquier momento. Mientras no autorices ninguna, ningún asistente tiene acceso a nada.

## URL de conexión

```
https://seuiot.com.br:8000/mcp
```

No pegas ninguna clave: el asistente descubre solo cómo iniciar sesión (OAuth 2.1 con PKCE) y abre una página de Seu IoT donde **tú** decides a qué puede acceder.

## Conecta tu asistente

| Cliente | Cómo |
|---|---|
| **Claude Code** | `claude mcp add --transport http seu-iot https://seuiot.com.br:8000/mcp`, luego ejecuta `/mcp` y autoriza en el navegador |
| **Claude.ai** | Configuración > Conectores > agregar un conector personalizado con la URL de arriba |
| **Gemini CLI** | En `settings.json`: `"mcpServers": { "seu-iot": { "httpUrl": "https://seuiot.com.br:8000/mcp" } }` |
| **Cursor** | En `mcp.json`: `"seu-iot": { "url": "https://seuiot.com.br:8000/mcp" }` |
| **ChatGPT** | Conectores MCP, donde tu cuenta tenga la función. Los Custom GPT Actions **aún no son compatibles** |

La compatibilidad con conectores MCP cambia rápido entre proveedores, así que revisa la documentación actual de tu cliente. Cualquier cliente que soporte MCP sobre HTTP con OAuth debería funcionar.

![Agregando el conector de Seu IoT en un asistente de IA (ejemplo: Claude.ai > Configuración > Conectores).](../../images/mcp-connect/01-add-connector.png)

## Autoriza la app

Cuando el asistente se conecta, el navegador abre una página de Seu IoT. Si no has iniciado sesión, hazlo primero. Después:

1. Revisa el nombre de la app. Lo informa la propia app y **Seu IoT no lo verificó**: autoriza solo si tú iniciaste esta conexión.
2. Elige **a qué proyectos** puede acceder. Ningún proyecto se libera por defecto. No necesitas liberar ninguno si permites que la app cree proyectos nuevos (pasa a acceder a los que cree).
3. En la tabla de permisos, elige **qué puede hacer** (mira abajo). Empieza por lo mínimo: puedes cambiarlo después.
4. Haz clic en **Autorizar**, o en **Denegar** para no compartir nada.

![La pantalla de autorización: nombre de la app, proyectos y permisos (abierta por el asistente).](../../images/mcp-connect/02-consent-screen.png)

## Permisos

| Permiso | La app puede |
|---|---|
| **Ver proyectos** | Listar tus proyectos liberados, con dispositivos, procesos y paneles (solo nombres y configuración) |
| **Leer datos** | Leer los datos recolectados por los procesos, incluidos resúmenes como promedio, mínimo y máximo |
| **Editar proyectos permitidos** | Crear y editar procesos, vínculos y gráficos dentro de los proyectos liberados. No incluye eliminar, ni enviar comandos a dispositivos |
| **Crear proyectos nuevos** | Crear proyectos nuevos en tu cuenta. Cada uno se libera a la app automáticamente. Incluye editar proyectos permitidos |
| **Eliminar procesos y vínculos** | *Pedir* eliminar procesos y vínculos. Cada eliminación sigue esperando tu aprobación |
| **Crear códigos de acceso** | *Pedir* la creación de contratos de acceso a datos (clave de API) y de widgets, y la emisión de su primera clave o token. Siempre necesita tu aprobación |
| **Ejecutar procesos (play)** | *Pedir* ejecutar un proceso ahora, como el botón de play |

Cada permiso tiene dos casillas:

- **Permitir**: la app puede hacerlo.
- **Pedir mi confirmación**: cada uso espera tu aprobación. Si la dejas sin marcar, la app aplica la acción al instante, bajo tu propia responsabilidad.

Una conexión nueva empieza con la confirmación marcada en todo. Leer no cambia nada, así que no tiene confirmación. En **Crear códigos de acceso**, la confirmación es siempre obligatoria.

![La tabla de permisos: Permitir y Pedir mi confirmación para cada permiso.](../../images/mcp-connect/03-permissions-table.png)

**Nunca permitido a ningún asistente de IA**: eliminar proyectos o dispositivos, eliminar datos recolectados, enviar comandos directos a actuadores fuera de un proceso, rotar claves, facturación y áreas de administración.

## Próximos pasos

- [Administrar apps conectadas](mcp-manage.md): aprobar cambios, editar permisos, ver qué hizo la app y revocar el acceso.
