# Dados em tempo real (MQTT)

Os valores ao vivo são entregues por um broker MQTT. O fluxo tem três passos, implementados em [`examples/python/mqtt-tls`](../../examples/python/mqtt-tls), [`examples/python/mqtt-websocket`](../../examples/python/mqtt-websocket) e [`examples/javascript/node-mqtt-websocket`](../../examples/javascript/node-mqtt-websocket):

1. `GET /external/v1/contract` para obter nomes e unidades.
2. `POST /external/v1/mqtt-credentials` para obter `username`, `password`, `host`, `ws_port` e `topics`.
3. Conectar e assinar **todos** os tópicos retornados.

## Tópicos e payload

Tópico: `/{project_id}/{device_uuid}/{process_uuid}/`

Quando o contrato não lista dispositivos, o nível do dispositivo no tópico é `+`: você recebe todos os dispositivos do projeto para aquele processo, e o dispositivo é identificado pelo tópico.

Payload: texto JSON, ex.: `{"answer_type": 1, "data": 22.4, "mode": 3, "id": 7, "timestamp": "31.01.2026 14:05:09.123456"}`. Use o escopo do contrato para transformar os uuids em nomes.

| Campo | Significado |
|---|---|
| `answer_type` | `1` = uma leitura (o que você quer). `0` = o dispositivo confirmando uma configuração: ignore |
| `data` | O valor. String, número ou booleano, conforme o tipo do processo |
| `mode` | Id numérico do tipo do processo |
| `id` | Revisão do processo que produziu o valor |
| `timestamp` | Hora do dispositivo em UTC, no formato do firmware `DD.MM.YYYY HH:MM:SS.microssegundos`. **Não é ISO 8601** |

A REST devolve timestamps ISO 8601 e o MQTT não, então normalize antes de misturar os dois. Exemplo de conversão: `31.01.2026 14:05:09.123456` vira `2026-01-31T14:05:09.123456Z`.

## Transportes

| Transporte | Porta | Certificado | Observação |
|---|---|---|---|
| MQTT sobre WebSocket (`wss`) | `ws_port` da resposta de credenciais (8084 em produção), caminho `/mqtt` | CA pública | Padrão, recomendado |
| MQTT sobre TLS (`mqtts`) | 8883 | pode ser autoassinado | Não vem na resposta de credenciais |

## Regras

- Cada `POST /mqtt-credentials` **rotaciona a senha**. Só peça uma nova credencial quando precisar de uma nova sessão ou após uma falha de autenticação.
- A credencial é **somente de assinatura** e restrita aos tópicos retornados. Assinar qualquer outro tópico faz o broker **desconectar** a sessão.
- Depois de alterar o escopo do contrato, peça uma nova credencial para obter a lista de tópicos atualizada.
- Use um `clientId` aleatório (ou acrescente um sufixo aleatório). Dois consumidores com o mesmo `clientId` se derrubam no broker.
- Assine dentro do evento `connect` do cliente, para que a assinatura seja restaurada a cada reconexão.
- Você **não** recebe o último valor ao assinar. Busque o valor atual uma vez pela REST (`limit=1`) e depois confie no MQTT.
- Depois de ficar offline, chame a REST **uma vez** com `start=<último timestamp processado>` para preencher a lacuna e volte ao MQTT. Nunca rode essa chamada em um timer.
- Se nada chegar, confira se o processo tem `publish_on_execute` habilitado e se o dispositivo está online.


## Revogação

O tópico `/broker/api-contract/<contract_uuid>/revoked` é sempre liberado. Uma mensagem nele significa que o contrato foi revogado ou excluído: feche o cliente e **não reconecte**. Veja [Ciclo de vida](lifecycle.md).
