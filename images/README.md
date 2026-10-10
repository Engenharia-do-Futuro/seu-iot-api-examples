# Images

Screenshots and GIFs used as a visual guide in the docs. They show where things are in the Seu IoT dashboard; they are not required to follow the docs.

The docs reference them with relative paths (`../../images/<page>/<file>`), so they render on GitHub and on the Seu IoT site (<https://seuiot.com.br/help-center/api-docs>). A reference whose file is not here yet is simply hidden on the site.

## Rules

- One folder per documentation page, one set of images shared by all languages.
- Names: `NN-short-description.png` for ordered steps, `short-description.png` otherwise. Lowercase, hyphens.
- Prefer PNG for screenshots and GIF for short flows (keep each file under about 2 MB).
- **Hide every secret** before saving: API keys (`siot_...`), MQTT passwords, widget tokens (`siotw_...`) and real hostnames or e-mails. Blur or replace them.
- The caption is the image's alt text in each `docs/<language>/*.md`; it should name the Seu IoT screen shown (for example "Dashboard > Project settings > API contracts").

## Checklist

| File | Page | What to capture |
|---|---|---|
| `getting-started/01-api-contracts-list.png` | getting-started | Project settings > API contracts, the contract list |
| `getting-started/02-create-contract.png` | getting-started | Creating a contract: name, processes and devices in scope |
| `getting-started/03-issue-key.png` | getting-started | Window shown after issuing the key (secrets hidden) |
| `widgets/01-widgets-tab.png` | widgets | The contract's Widgets tab |
| `widgets/02-create-widget.png` | widgets | Creating a widget: chart type, signals, devices |
| `widgets/03-embed-code.png` | widgets | The code icon (`</>`) window with the embed tag (token hidden) |
| `lifecycle/contract-actions.png` | lifecycle | Contract actions in the list: revoke, reactivate, delete |
| `lifecycle/usage-window.png` | lifecycle | The contract usage window (30 days and daily series) |
| `mcp-connect/01-add-connector.png` | mcp-connect | Adding the Seu IoT connector in an AI assistant (for example Claude.ai > Settings > Connectors) |
| `mcp-connect/02-consent-screen.png` | mcp-connect | The authorization screen: app name, projects, permissions |
| `mcp-connect/03-permissions-table.png` | mcp-connect | The permissions table with Allow and Ask for my confirmation |
| `mcp-manage/01-connected-apps-list.png` | mcp-manage | Configuration > Connected apps, the list of apps |
| `mcp-manage/02-pending-approval.png` | mcp-manage | Pending changes: the bell in Notifications and the "Changes waiting for your approval" card |
| `mcp-manage/03-review-change.png` | mcp-manage | The review window of a change proposed by an AI app |
| `mcp-manage/04-credential-delivery.png` | mcp-manage | Approving a key, with the "hand the credential straight to the app" option (secrets hidden) |
| `mcp-manage/05-edit-permissions.png` | mcp-manage | The Edit permissions window |
| `mcp-manage/06-activity-log.png` | mcp-manage | The "What this app did" window |
| `mcp-manage/07-revoke.png` | mcp-manage | The revoke confirmation (typing the app name) |
