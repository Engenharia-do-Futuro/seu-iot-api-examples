# Conectar uma IA (MCP)

Assistentes de IA como Claude, Cursor ou Gemini CLI podem trabalhar com a sua conta do Seu IoT por meio do **MCP** (Model Context Protocol). O assistente é apenas mais uma interface para a sua conta: ele só enxerga os projetos que você liberar, só faz o que você permitir, e tudo que é sensível espera a sua aprovação no painel.

Isso é diferente dos [contratos de API](getting-started.md). Um contrato deixa um *sistema externo* ler dados com uma chave de API. O MCP deixa um *assistente de IA* trabalhar dentro da sua conta (listar projetos, ler dados, criar processos e gráficos, até pedir um contrato). Um assistente também pode criar contratos para você, com a sua aprovação.

## Não há nada para habilitar

Não existe um botão para ligar. A conexão só existe quando você **autoriza um app**, e você pode revogá-la a qualquer momento. Enquanto você não autorizar nenhum, nenhum assistente tem acesso a nada.

## URL de conexão

```
https://seuiot.com.br:8000/mcp
```

Você não cola nenhuma chave: o assistente descobre sozinho como entrar (OAuth 2.1 com PKCE) e abre uma página do Seu IoT onde **você** decide o que ele pode acessar.

## Conecte o seu assistente

| Cliente | Como |
|---|---|
| **Claude Code** | `claude mcp add --transport http seu-iot https://seuiot.com.br:8000/mcp`, depois rode `/mcp` e autorize no navegador |
| **Claude.ai** | Configurações > Conectores > adicionar um conector personalizado com a URL acima |
| **Gemini CLI** | No `settings.json`: `"mcpServers": { "seu-iot": { "httpUrl": "https://seuiot.com.br:8000/mcp" } }` |
| **Cursor** | No `mcp.json`: `"seu-iot": { "url": "https://seuiot.com.br:8000/mcp" }` |
| **ChatGPT** | Conectores MCP, onde a sua conta tiver o recurso. Os Custom GPT Actions **ainda não são suportados** |

O suporte a conectores MCP muda rápido entre os fornecedores, então confira a documentação atual do seu cliente. Qualquer cliente que suporte MCP sobre HTTP com OAuth deve funcionar.

![Adicionando o conector do Seu IoT em um assistente de IA (exemplo: Claude.ai > Configurações > Conectores).](../../images/mcp-connect/01-add-connector.png)

## Autorize o app

Quando o assistente se conecta, o navegador abre uma página do Seu IoT. Se você não estiver logado, entre primeiro. Depois:

1. Confira o nome do app. Ele é informado pelo próprio app e **não foi verificado pelo Seu IoT**: autorize apenas se foi você quem iniciou esta conexão.
2. Escolha **quais projetos** o app pode acessar. Nenhum projeto é liberado por padrão. Você não precisa liberar nenhum se permitir que o app crie projetos novos (ele passa a acessar os que criar).
3. Na tabela de permissões, escolha **o que ele pode fazer** (veja abaixo). Comece pelo mínimo: você pode mudar depois.
4. Clique em **Autorizar**, ou em **Negar** para não compartilhar nada.

![A tela de autorização: nome do app, projetos e permissões (aberta pelo assistente).](../../images/mcp-connect/02-consent-screen.png)

## Permissões

| Permissão | O app pode |
|---|---|
| **Ver projetos** | Listar seus projetos liberados, com dispositivos, processos e painéis (somente nomes e configuração) |
| **Ler dados** | Ler os dados coletados pelos processos, inclusive resumos como média, mínimo e máximo |
| **Editar projetos liberados** | Criar e editar processos, ligações e gráficos dentro dos projetos liberados. Não inclui apagar, nem enviar comandos a dispositivos |
| **Criar novos projetos** | Criar projetos novos na sua conta. Cada um é liberado ao app automaticamente. Inclui editar projetos liberados |
| **Apagar processos e ligações** | *Pedir* para apagar processos e ligações. Cada exclusão continua esperando a sua aprovação |
| **Criar códigos de acesso** | *Pedir* a criação de contratos de acesso a dados (chave de API) e de widgets, e a emissão da primeira chave ou token. Sempre precisa da sua aprovação |
| **Executar processos (play)** | *Pedir* para executar um processo agora, como no botão de play |

Cada permissão tem duas caixas:

- **Permitir**: o app pode fazer isso.
- **Pedir minha confirmação**: cada uso espera a sua aprovação. Se você deixar desmarcada, o app aplica a ação na hora, por sua conta e risco.

Uma conexão nova começa com a confirmação marcada em tudo. Leitura não altera nada, então não tem confirmação. Em **Criar códigos de acesso**, a confirmação é sempre obrigatória.

![A tabela de permissões: Permitir e Pedir minha confirmação para cada permissão.](../../images/mcp-connect/03-permissions-table.png)

**Nunca permitido a nenhum assistente de IA**: apagar projetos ou dispositivos, apagar dados coletados, enviar comandos direto a atuadores fora de um processo, rotacionar chaves, faturamento e áreas de administração.

## Próximos passos

- [Gerenciar apps conectados](mcp-manage.md): aprovar alterações, editar permissões, ver o que o app fez e revogar o acesso.
