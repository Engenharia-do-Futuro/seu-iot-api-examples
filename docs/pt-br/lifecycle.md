# Ciclo de vida: expiração, rotação, revogação e uso

## Expiração

A chave de API, e o login MQTT que vem com ela, valem **365 dias**. Depois disso, a REST responde `401` e o MQTT recusa a conexão. Emita uma nova chave no painel. O `embed_token` de um widget também dura 365 dias.

## Rotação

A rotação é feita no painel. Ela regenera a chave de API **e** o login MQTT juntos. Os anteriores deixam de funcionar na hora, sem período de sobreposição, então atualize os segredos do seu consumidor logo em seguida.

Chamar `POST /external/v1/mqtt-credentials` (ou o `/bootstrap` público de um widget) também rotaciona a senha MQTT. Evite isso em código em execução.

## Revogação

- **Revogar** um contrato: a REST responde `401` imediatamente, o login MQTT é desabilitado, os consumidores conectados recebem uma mensagem em `/broker/api-contract/<contract_uuid>/revoked` e são desconectados, e os widgets do contrato são desligados.
- **Reativar** traz de volta a **mesma** chave e o mesmo login MQTT. Os widgets continuam desligados até o dono reativar cada um.
- **Excluir** um contrato o manda para a lixeira: ele para de funcionar imediatamente e é apagado depois.
- Um consumidor que recebe a mensagem de revogação deve parar e **não** tentar de novo.

![Ações do contrato na lista: revogar, reativar e excluir.](../../images/lifecycle/contract-actions.png)

## Mudanças de escopo

Editar os processos e dispositivos do contrato é feito no painel. Remover itens vale na próxima chamada REST e desconecta os consumidores MQTT ao vivo, que reconectam com a lista de tópicos menor.

## Acompanhar o uso

O painel mostra, por contrato, as requisições REST de hoje e dos últimos 30 dias, e os carregamentos de widget, com uma série diária. O MQTT não é contado.

Se o número da REST cresce sem parar quando você esperava atualizações ao vivo, algum consumidor está fazendo polling: troque-o por uma assinatura [MQTT](realtime-mqtt.md).

![A janela de uso de um contrato: requisições de hoje e dos últimos 30 dias, com série diária.](../../images/lifecycle/usage-window.png)

## Limites de um contrato

- Pertence a **um projeto**. Para dois projetos, crie dois contratos.
- Nome: até 100 caracteres.
- Escopo: de 1 a 50 processos e até 50 dispositivos. Qualquer dispositivo listado pode ser lido para qualquer processo listado. Sem dispositivos listados, todos os do projeto entram, inclusive os adicionados depois.
