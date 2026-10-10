# Widgets embutíveis

Um widget é um gráfico que você cola em qualquer página web com uma tag `<script>`. Exemplo: [`examples/web/widget-embed`](../../examples/web/widget-embed).

## Criar o widget

1. Painel > Configurações do projeto > Contratos de API > seu contrato > aba **Widgets**.
2. Crie um widget para um dos sinais do escopo do contrato.
3. Clique no ícone de código (`</>`), gere o `embed_token` e copie a tag.

## Embutir

```html
<script src="https://seuiot.com.br:8000/widgets/v1/embed.js"
        data-widget="siotw_..." async></script>
```

O script insere um `<iframe>` logo após si mesmo, isolado do CSS e JavaScript da sua página, e o redimensiona conforme o conteúdo. Um token inválido, revogado ou expirado mostra um erro visível em vez de uma área em branco.

## Tema

- Padrão: segue a preferência de sistema/navegador do visitante (`prefers-color-scheme`).
- `data-theme="light"` ou `"dark"` no `<script>` força um tema inicial.
- Troca ao vivo pela sua página, sem recarregar:

```js
window.SeuIoTWidget.setTheme("siotw_...", "dark"); // ou "light"
```

O `embed.js` carrega com `async`; chamadas feitas antes de ele terminar de carregar são ignoradas.

## Notas de segurança

- O `embed_token` é público por design e só expõe os sinais daquele widget. Nunca é a sua chave de API.
- `/widgets/v1/embed.js` é servido com CORS aberto para qualquer origem. Todas as outras rotas exigem sessão ou chave de API.
- Para impedir que um widget funcione, revogue ou exclua-o no painel.

## Limites e ciclo de vida

- Um widget mostra de 1 a 20 dispositivos, todos dentro dos dispositivos do contrato. Com vários, o visitante escolhe qual ver.
- Qualquer tipo de gráfico, exceto `table` e `geo_map`. As cores devem ser hex (`#rrggbb`) ou nome de cor, porque o widget é renderizado em página pública.
- O `embed_token` vale 365 dias.
- Revogar o contrato desliga seus widgets, inclusive para visitantes que já estão na página. Reativar o contrato **não** religa os widgets: o dono revisa e reativa cada um.
- Não atualize a página em um timer nem chame as rotas públicas `/bootstrap` e `/data` do widget a partir do seu código: o widget já se atualiza sozinho por MQTT, o `/bootstrap` substitui a senha MQTT do widget para todos os visitantes, e cada carregamento conta no uso do contrato.
