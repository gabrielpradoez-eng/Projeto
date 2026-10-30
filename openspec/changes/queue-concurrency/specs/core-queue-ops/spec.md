## ADDED Requirements

### Requirement: Queue mutations serialize shared resources
O backend MUST serializar a alocação de número e a seleção/mutação de atendimento por fila. O estado usado nas precondições MUST ser lido após obter o bloqueio, dentro da transação.

#### Scenario: Emissões simultâneas
- **WHEN** duas solicitações autorizadas emitem na mesma fila aberta
- **THEN** as respostas bem-sucedidas usam números distintos sem falha causada por leitura concorrente do último número.

#### Scenario: Chamadas simultâneas
- **WHEN** solicitações concorrentes tentam iniciar atendimento na mesma fila
- **THEN** a mesma senha não gera atendimentos duplicados e a regra operacional de atendimento ativo é preservada.

#### Scenario: Conclusão repetida
- **WHEN** duas solicitações tentam concluir o mesmo atendimento
- **THEN** a primeira conclusão válida é persistida e a seguinte observa o estado atualizado antes de alterar registros.

### Requirement: Attendant registration serializes the candidate account
O backend MUST serializar a verificação e criação de vínculo pela conta candidata, sem ampliar permissões além da confirmação administrativa.

#### Scenario: Vínculos simultâneos
- **WHEN** dois administradores autorizados tentam cadastrar a mesma conta cliente
- **THEN** no máximo um vínculo é criado e a segunda solicitação observa o perfil ou vínculo já atualizado.
