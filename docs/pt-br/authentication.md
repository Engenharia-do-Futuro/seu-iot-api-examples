# Autenticação

O Seu IoT tem dois tipos de credencial, que não são intercambiáveis.

| | Chave de API | `embed_token` de widget |
|---|---|---|
| Formato | `siot_...` | `siotw_...` |
| Usada por | seu **servidor** ou scripts | o **navegador** do visitante |
| Enviada como | `Authorization: Bearer <chave>` | parte da tag do widget |
| Expõe | todo o escopo do contrato | só os sinais de um widget |
| Secreta? | **Sim** | Não, feita para ser pública |

## Regras para a chave de API

- Envie-a **somente** no cabeçalho `Authorization: Bearer`. Chaves na query string (`api_key`, `token`, `access_token`, `key`) são rejeitadas com `400`.
- Nunca coloque em código de front-end, apps móveis ou repositórios públicos. Use variáveis de ambiente (veja o `.env.example` de cada exemplo).
- Uma chave revogada, inativa ou expirada retorna `401`.
- As requisições têm limite de taxa por contrato (atualmente 60 por minuto); o excesso retorna `429`.

## Credenciais MQTT

`POST /external/v1/mqtt-credentials` troca a chave de API por usuário/senha do broker. **Cada chamada rotaciona a senha**: a credencial MQTT anterior deixa de funcionar. Veja [Tempo real](realtime-mqtt.md).
