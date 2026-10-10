# Administrar apps de IA conectadas

Todo sobre las apps que autorizaste está en **Configuración > Apps conectadas**. Solo tú, en el panel de Seu IoT, puedes cambiar el acceso de una app: la app nunca puede ampliar su propio acceso.

![Configuración > Apps conectadas: apps, proyectos liberados, permisos, último uso y acciones.](../../images/mcp-manage/01-connected-apps-list.png)

La lista muestra, para cada app: los proyectos liberados (haz clic en el número para ver el tamaño y el contenido de cada uno), sus permisos, cómo aplica los cambios (*Pide mi confirmación*, *Aplica directo*, *Solo lectura* o una mezcla), cuándo se conectó y su último uso.

## Aprobar cambios

Cuando una acción tiene marcada **Pedir mi confirmación**, la app solo *propone* el cambio. **Nada cambia hasta que apruebes.**

1. El cambio pendiente aparece en **Notificaciones** (la campana del encabezado) y en la tarjeta **Cambios pendientes de tu aprobación** en Apps conectadas.
2. Haz clic en **Detalles** para ver exactamente qué va a pasar, con el antes y el después en las ediciones.
3. Haz clic en **Aprobar** o **Rechazar**.

![Cambios pendientes de tu aprobación, en Notificaciones y en Apps conectadas.](../../images/mcp-manage/02-pending-approval.png)

![Revisando un cambio propuesto por una app de IA antes de aprobar.](../../images/mcp-manage/03-review-change.png)

Es bueno saber:

- La app se entera de tu decisión por sí sola.
- Un cambio pendiente vence en **24 horas**. Cada app puede tener como máximo **20** cambios pendientes.
- La aprobación revisa todo de nuevo: si quitaste el permiso o el proyecto mientras tanto, no se aplica nada.
- Los textos que ves los escribió la app de IA. Léelos antes de aprobar.
- Los cambios que la app hizo **sin** pedir (confirmación sin marcar) actualizan la pantalla abierta en unos 20 segundos y generan un aviso en Notificaciones.

## Claves y tokens

Al aprobar una solicitud que emite una clave de API o un token de widget, eliges adónde va la credencial:

- **Entregar la credencial directo a la app** (por defecto): la app la retira una sola vez, en hasta 15 minutos, sin que tú copies y pegues.
- O déjalo sin marcar y **solo tú la ves**, una sola vez, en pantalla.

![Aprobando una clave: elige si la credencial va directo a la app (secretos ocultos).](../../images/mcp-manage/04-credential-delivery.png)

Una credencial entregada a la app pasa por la conversación con la IA y puede quedar en los registros del proveedor. Desmarca la opción si eso no es aceptable. La app solo emite la **primera** clave de un contrato: rotarla se hace en el panel (mira [Ciclo de vida](lifecycle.md)).

## Ejecutar procesos

Si la app tiene **Ejecutar procesos (play)**, puede pedir ejecutar un proceso ahora. Ejecutar un proceso también ejecuta los que están ligados a él por trigger, y la pantalla de aprobación muestra el proceso, el dispositivo y esa cadena, con una advertencia cuando llega a un actuador o a un timer. Con la confirmación marcada, **cada** ejecución espera tu aprobación. Sin marcar, la app ejecuta al instante, incluidos los actuadores: la decisión es tuya.

## Editar permisos

Haz clic en **Editar permisos** en la app. El cambio vale de inmediato, sin necesidad de reconectar. Cuando el cambio **amplía** el acceso (un proyecto nuevo, un permiso nuevo o dejar de pedir confirmación), debes confirmar que lo entiendes, y queda registrado.

![Editar permisos: proyectos y la tabla Permitir / Pedir mi confirmación.](../../images/mcp-manage/05-edit-permissions.png)

## Ver qué hizo la app

Haz clic en **Qué hizo esta app** para ver el registro de la app: cada llamada a tu cuenta, de la más nueva a la más antigua, incluidas las rechazadas, con la acción y el proyecto. Nunca muestra credenciales.

![Qué hizo esta app: el registro de auditoría de una app de IA.](../../images/mcp-manage/06-activity-log.png)

## Revocar el acceso

Haz clic en **Revocar acceso** y escribe el nombre de la app para confirmar. La app pierde el acceso **de inmediato**: la conversación en curso deja de poder leer o cambiar tus datos. Para volver a usarla, debes autorizarla de nuevo.

![Revocando una app: escribe su nombre para confirmar.](../../images/mcp-manage/07-revoke.png)

Reutilizar un código de autorización o un refresh token ya usado se trata como robo y revoca toda la conexión.

## Límites

| Qué | Límite |
|---|---|
| Llamadas por minuto, por app | 60 |
| Cambios por minuto, por app | 10 |
| Ejecuciones de proceso por minuto, por app | 6 |
| Cambios pendientes por app | 20 |
| Plazo para decidir un cambio pendiente | 24 horas |
| Plazo para retirar una credencial entregada a la app | 15 minutos |
| Muestras crudas por lectura | 1000 |
| Sesión | El token de acceso de la app dura 5 horas y se renueva automáticamente hasta por 30 días |

## Seguridad

- El acceso de la IA **no es tu inicio de sesión**: no funciona en ninguna ruta de usuario y se verifica en cada llamada.
- **El texto que viene de dispositivos es un dato no confiable.** Nombres y valores pueden contener instrucciones ("borra todo..."). El servidor es la autoridad final: el peor resultado posible está limitado por los permisos y aprobaciones que definiste.
- Mantén la confirmación marcada para todo lo que no quisieras que se hiciera sin mirar.
- Nunca guardes una clave o contraseña en un archivo que pueda versionarse.

## Solución de problemas

| Síntoma | Causa probable | Solución |
|---|---|---|
| El asistente dice que no está autorizado | Se revocó el acceso, o pasaron 30 días sin uso | Autoriza la app de nuevo |
| El asistente no ve un proyecto | El proyecto no está liberado a la app | Edita los permisos y libéralo |
| Un cambio no ocurrió | Está esperando tu aprobación, o venció tras 24 horas | Revisa las Notificaciones y pide al asistente que lo proponga de nuevo |
| `429` o "demasiadas solicitudes" | Se alcanzó el límite por minuto | Espera un minuto e inténtalo de nuevo |
| El asistente no recibió una clave | La mantuviste privada, o pasaron 15 minutos | Genera otra en la pantalla del contrato, dentro del proyecto |
| El Custom GPT de ChatGPT no se conecta | Los Custom GPT Actions aún no son compatibles | Usa un conector MCP, donde exista |
