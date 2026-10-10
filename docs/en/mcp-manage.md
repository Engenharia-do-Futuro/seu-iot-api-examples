# Manage connected AI apps

Everything about the apps you authorized is in **Configuration > Connected apps**. Only you, in the Seu IoT dashboard, can change an app's access: the app can never widen its own.

![Configuration > Connected apps: apps, released projects, permissions, last use and actions.](../../images/mcp-manage/01-connected-apps-list.png)

The list shows, for each app: the released projects (click the number to see the size and content of each one), its permissions, how it applies changes (*Asks for my confirmation*, *Applies directly*, *Read only* or a mix), when it connected and its last use.

## Approve changes

When an action has **Ask for my confirmation** checked, the app only *proposes* it. **Nothing changes until you approve.**

1. The pending change appears in **Notifications** (the bell in the header) and in the card **Changes waiting for your approval** in Connected apps.
2. Click **Details** to see exactly what will happen, with the before and after for edits.
3. Click **Approve** or **Reject**.

![Changes waiting for your approval, in Notifications and in Connected apps.](../../images/mcp-manage/02-pending-approval.png)

![Reviewing a change proposed by an AI app before approving.](../../images/mcp-manage/03-review-change.png)

Good to know:

- The app finds out your decision by itself.
- A pending change expires after **24 hours**. Each app can have at most **20** pending changes.
- Approval checks everything again: if you removed the permission or the project in the meantime, nothing is applied.
- The texts you see were written by the AI app. Read them before approving.
- Changes the app made **without** asking (confirmation unchecked) update the open screen within about 20 seconds and generate a notice in Notifications.

## Keys and tokens

When you approve a request that issues an API key or a widget token, you choose where the credential goes:

- **Hand the credential straight to the app** (default): the app retrieves it once, within 15 minutes, without you copying and pasting.
- Or leave it unchecked and **only you see it**, once, on the screen.

![Approving a key: choose whether the credential goes straight to the app (secrets hidden).](../../images/mcp-manage/04-credential-delivery.png)

A credential handed to the app passes through the conversation with the AI and may stay in the provider's logs. Uncheck the option if that is not acceptable. The app only issues the **first** key of a contract: rotating it is done in the dashboard (see [Lifecycle](lifecycle.md)).

## Running processes

If the app has **Run processes (play)**, it can ask to run a process now. Running a process also runs the ones linked to it by trigger, and the approval screen shows the process, the device and that chain, with a warning when it reaches an actuator or a timer. With confirmation checked, **every** run waits for your approval. Unchecked, the app runs immediately, including actuators: it is your choice.

## Edit permissions

Click **Edit permissions** on the app. The change applies right away, with no need to reconnect. When the change **widens** access (a new project, a new permission or no more confirmation), you must acknowledge it, and it is recorded.

![Edit permissions: projects and the Allow / Ask for my confirmation table.](../../images/mcp-manage/05-edit-permissions.png)

## See what the app did

Click **What this app did** to see the app's log: every call to your account, newest first, including refused ones, with the action and the project. It never shows credentials.

![What this app did: the audit log of an AI app.](../../images/mcp-manage/06-activity-log.png)

## Revoke access

Click **Revoke access** and type the app's name to confirm. The app loses access **immediately**: the conversation in progress can no longer read or change your data. To use it again you must authorize it again.

![Revoking an app: type its name to confirm.](../../images/mcp-manage/07-revoke.png)

Reusing an authorization code or a refresh token that was already used is treated as theft and revokes the whole connection.

## Limits

| What | Limit |
|---|---|
| Calls per minute, per app | 60 |
| Changes per minute, per app | 10 |
| Process runs per minute, per app | 6 |
| Pending changes per app | 20 |
| Time to decide on a pending change | 24 hours |
| Time to retrieve a credential handed to the app | 15 minutes |
| Raw samples per read | 1000 |
| Session | The app's access token lasts 5 hours and is renewed automatically for up to 30 days |

## Security

- The AI's access is **not your login**: it does not work on any user route, and it is checked on every call.
- **Text coming from devices is untrusted data.** Names and values can contain instructions ("delete everything..."). The server is the final authority: the worst outcome is limited by the permissions and approvals you set.
- Keep confirmation checked for anything you would not want done without looking.
- Never save a key or password in a file that can be committed.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| The assistant says it is unauthorized | Access was revoked, or 30 days passed without use | Authorize the app again |
| The assistant does not see a project | The project is not released to the app | Edit permissions and release it |
| A change did not happen | It is waiting for your approval, or it expired after 24 hours | Check Notifications and ask the assistant to propose it again |
| `429` or "too many requests" | Per-minute limit reached | Wait a minute and try again |
| The assistant did not receive a key | You kept it private, or 15 minutes passed | Generate another in the contract's screen in the project |
| ChatGPT custom GPT does not connect | Custom GPT Actions are not supported yet | Use an MCP connector, where available |
