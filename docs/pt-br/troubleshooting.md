# Solução de problemas

| Sintoma | Causa provável | Solução |
|---|---|---|
| `401` em qualquer chamada | Chave ausente, digitada errada, revogada ou expirada | Confira o cabeçalho `Authorization: Bearer siot_...` e o status do contrato no painel |
| `400` "API key must be sent via the Authorization header" | Chave enviada na query string | Mova para o cabeçalho |
| `404` em `/processes/{uuid}/data` | Processo ou dispositivo fora do escopo | Liste o escopo com `GET /contract` e edite o contrato se necessário |
| `429` | Mais de 60 requisições por minuto no contrato | Espere e tente de novo; prefira MQTT para dados ao vivo em vez de polling |
| MQTT desconecta logo após assinar | Assinou um tópico que não está na lista retornada | Assine só os `topics` da credencial mais recente |
| Autenticação MQTT falha depois de funcionar | Outro `POST /mqtt-credentials` rotacionou a senha | Use a credencial da chamada mais recente; não rode dois clientes no mesmo contrato com handshakes separados |
| Widget mostra um erro | Token inválido, revogado ou expirado | Gere o token de novo; veja [Widgets](widgets.md) |
| Nomes aparecem como uuids | Processo/dispositivo foi removido do projeto | Atualize o escopo do contrato |
| Nenhum valor chega por MQTT | O processo não publica, ou o dispositivo está offline | Confira se o processo tem `publish_on_execute` habilitado e se o dispositivo está online |
| O MQTT para e chega uma mensagem em `.../revoked` | O contrato foi revogado ou excluído | Pare e não reconecte; veja [Ciclo de vida](lifecycle.md) |
| O timestamp do MQTT não vira data | O MQTT usa o formato do firmware `DD.MM.YYYY HH:MM:SS.ffffff` | Converta para ISO 8601; veja [Tempo real](realtime-mqtt.md) |
| `401` depois de cerca de um ano | A chave (e o login MQTT) vale 365 dias | Emita uma nova chave no painel |
