## ADDED Requirements

### Requirement: Chat privado de atendimento
O portal MUST disponibilizar mensagens apenas ao cliente titular da senha e ao atendente ativo vinculado ao atendimento em curso.

#### Scenario: Senha chamada
- **WHEN** o atendente chama uma senha emitida pelo cliente autenticado
- **THEN** os dois participantes podem consultar e enviar mensagens de até 500 caracteres no chat do atendimento.

#### Scenario: Antes ou depois do atendimento
- **WHEN** a senha aguarda chamada ou o atendimento já foi concluído
- **THEN** o backend não permite ler nem enviar mensagens daquela conversa.

#### Scenario: Acesso de terceiros
- **WHEN** outra conta tenta acessar o chat ou apresenta somente uma referência de rastreamento
- **THEN** o backend rejeita o acesso sem revelar o conteúdo.
