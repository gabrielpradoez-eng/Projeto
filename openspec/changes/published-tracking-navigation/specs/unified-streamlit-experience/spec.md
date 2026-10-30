## ADDED Requirements

### Requirement: Navegação após emissão sem perda do comprovante
O sistema MUST permitir alternar entre emissão e acompanhamento sem erro de estado nem perda da referência confirmada.

#### Scenario: Navegação após emissão sem perda do comprovante
- **WHEN** o cliente seleciona acompanhar após emitir uma senha
- **THEN** o acompanhamento usa a referência confirmada e a navegação não falha.

### Requirement: Atualização encerrada após limpeza da sessão
O sistema MUST interromper atualizações agendadas quando a sessão ou a referência de acompanhamento deixar de existir.

#### Scenario: Atualização encerrada após limpeza da sessão
- **WHEN** uma atualização agendada executa após logout ou encerramento do acompanhamento
- **THEN** nenhuma consulta é enviada e nenhuma exceção de referência ausente é exibida.

### Requirement: Feed com horário canônico
O sistema MUST aceitar horários válidos retornados pelo feed e preservar a ordenação canônica.

#### Scenario: Feed com horário canônico
- **WHEN** o feed retorna horário UTC em milissegundos e uma primeira chamada após snapshot vazio
- **THEN** a chamada é apresentada com horário válido.
