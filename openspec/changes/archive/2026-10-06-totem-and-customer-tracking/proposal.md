## Why

Clientes precisam emitir uma senha presencialmente com poucos passos e acompanhar seu status e posição enquanto aguardam atendimento. Hoje o protótipo Streamlit reúne a emissão em uma aba genérica e não oferece acompanhamento individual; esta mudança define uma experiência dedicada sem deslocar para a interface a autoridade sobre filas e senhas.

## What Changes

- Criar uma interface Streamlit de Totem com seleção de serviço/fila disponíveis e confirmação clara da senha emitida.
- Oferecer ao cliente uma tela de acompanhamento de uma senha, exibindo status, posição na fila e estimativa quando fornecida pelo backend; encerrar a referência quando a senha for concluída ou após 24 horas da emissão, o que ocorrer primeiro.
- Definir contratos Xano para emissão e consulta individual do acompanhamento, incluindo autorização e cálculo server-side de posição/estimativa.
- Exibir estados de carregamento, fila indisponível, referência inválida e falha temporária, com atualização periódica dos dados fornecidos pelo backend.
- Fora de escopo: painel público de chamadas, painel de atendente, notificações push/SMS, aplicação mobile nativa, pagamentos e definição de políticas de prioridade ou previsão de espera.

## Capabilities

### New Capabilities
- `totem-customer-tracking`: emissão simplificada de senha no Totem Streamlit e acompanhamento individual de status e posição, usando o Xano como fonte de verdade.

### Modified Capabilities

## Impact

- Streamlit: separar os fluxos de Totem e acompanhamento do restante do protótipo e consumir contratos Xano sem replicar regras de fila.
- Xano: ampliar os endpoints de gestão de filas para disponibilizar filas elegíveis para emissão e uma consulta individual segura de senha/status/posição/estimativa. O endpoint atual `join` exige autenticação de usuário e `stats` retorna estatísticas agregadas, não a posição de uma senha específica.
- Dados: usar senha, fila e usuário já existentes; a referência de acompanhamento deve ser não previsível e validada pelo backend, sem expor credenciais nem permitir consulta de senhas de terceiros.
- Premissa: o Totem será provisionado como cliente confiável sem credencial de usuário visível ao público; o Xano será responsável por autorizar a emissão e emitir uma referência segura para acompanhamento. A forma exata dessa credencial/identidade deve ser confirmada ao implementar a integração real.