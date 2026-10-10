# API REST

URL base: seu servidor Seu IoT, ex.: `https://seuiot.com.br:8000`. Todas as rotas ficam em `/external/v1` e exigem `Authorization: Bearer <chave de API>`.

## GET /external/v1/contract

Retorna o contrato dono da chave e seu escopo, já resolvido para nomes.

```bash
curl -H "Authorization: Bearer $SIOT_API_KEY" "$SIOT_API_BASE_URL/external/v1/contract"
```

```json
{
  "uuid": "...",
  "name": "Meu contrato",
  "process_uuids": ["..."],
  "device_uuids": ["..."],
  "processes": [{ "uuid": "...", "name": "Temperatura", "unit": "C" }],
  "devices": [{ "uuid": "...", "name": "Sensor da estufa 1" }],
  "is_active": true,
  "expires_at": "2027-01-01T00:00:00"
}
```

- `device_uuids` vazio significa **todos os dispositivos** do projeto.
- `unit` só existe para processos do tipo Linearização.
- `name` é `null` se o processo/dispositivo foi removido do projeto depois de entrar no escopo.

## GET /external/v1/processes/{process_uuid}/data

Dados históricos de um processo.

| Parâmetro de query | Descrição |
|---|---|
| `device_uuid` | Somente este dispositivo (deve estar no escopo) |
| `start`, `end` | Intervalo de tempo, ISO 8601 em UTC, ambos inclusivos |
| `limit` | Máximo de pontos. Padrão `500`, máximo `2000` |

```bash
curl -H "Authorization: Bearer $SIOT_API_KEY" \
  "$SIOT_API_BASE_URL/external/v1/processes/$PROCESS_UUID/data?limit=20"
```

```json
[{ "data": "22.4", "timestamp": "2026-09-30T12:00:00", "mode": 0, "device_uuid": "..." }]
```

Os `limit` pontos mais recentes são retornados em **ordem cronológica** (do mais antigo ao mais novo). Observações:

- `data` é uma string; o formato depende do tipo do processo.
- `mode` é o id numérico do tipo do processo.
- Cada ponto traz o `device_uuid` de onde veio, então uma chamada pode cobrir vários dispositivos. Sem o parâmetro `device_uuid` você recebe os dispositivos que o contrato permite (todos os do projeto, se ele não listar nenhum).
- Para o último valor, use `limit=1`.
- Não há paginação por cursor. Para percorrer mais de 2000 pontos, avance o histórico em janelas de tempo com `start` e `end` (ambos são inclusivos, então descarte o ponto repetido na fronteira).

## POST /external/v1/mqtt-credentials

Emite ou rotaciona a credencial MQTT. Retorna `201`:

```json
{
  "username": "...",
  "password": "...",
  "host": "mqtt.seuiot.com.br",
  "ws_port": 8084,
  "topics": ["/12/device-uuid/process-uuid/"]
}
```

A senha aparece **somente nesta resposta**. Cada chamada a substitui, então não chame esta rota na partida de um consumidor. Veja [Tempo real](realtime-mqtt.md).

## Limites

- **60 requisições por minuto** por contrato; acima disso a API responde `429`.
- Cada requisição autorizada é contada por dia UTC no uso do contrato. O tráfego MQTT não é contado.
- A chave vale **365 dias** a partir da emissão; depois disso a API responde `401`.
- Use REST para histórico e para o primeiro valor. Para receber valores novos, não faça polling: use [MQTT](realtime-mqtt.md).

## Erros

Os erros retornam JSON com `message`, `status` e `error_code`.

| HTTP | `error_code` | Significado |
|---|---|---|
| 400 | `API_CONTRACT_UNAUTHORIZED` | Chave de API enviada na query string |
| 401 | `API_CONTRACT_UNAUTHORIZED` | Chave ausente, inválida, revogada ou expirada |
| 404 | `EXTERNAL_API_PROCESS_NOT_IN_SCOPE` | Processo fora do escopo do contrato |
| 404 | `EXTERNAL_API_DEVICE_NOT_IN_SCOPE` | Dispositivo fora do escopo do contrato |
| 429 | `API_CONTRACT_RATE_LIMITED` | Requisições demais, tente novamente em instantes |

Recursos fora do escopo retornam `404`, não `403`, para que a API nunca revele se eles existem.
