# Core Queue Operations Specification

## Purpose
Define the baseline operational capabilities of the FilaSmart core: authentication, user roles, establishment and service setup, queue lifecycle, ticket issuance, attendant calling flow, and service completion with auditing.

## Requirements

### Requirement: Authentication and role-based access
The system SHALL authenticate users with valid credentials and restrict protected actions according to role and establishment ownership.

#### Scenario: Successful login
- **WHEN** a registered user submits valid credentials
- **THEN** the system SHALL return an authenticated session containing the user identity and role.

#### Scenario: Unauthorized operation
- **WHEN** a user attempts an action outside their permissions
- **THEN** the system SHALL reject the request and record the action in the audit log.

### Requirement: Establishment and service setup
The system SHALL support the registration of establishments and the definition of services tied to those establishments.

#### Scenario: Register service
- **WHEN** an administrator creates a service for an establishment
- **THEN** the service SHALL be linked to that establishment and store the estimated handling time.

### Requirement: Queue lifecycle and ticket issuance
The system SHALL support open and closed queues and generate sequential ticket numbers within each queue.

#### Scenario: Ticket emission
- **WHEN** a valid user requests a ticket in an open queue
- **THEN** the system SHALL assign the next available number and persist the ticket in waiting status.

### Requirement: Queue calling and attendance workflow
The system SHALL allow an active attendant to call the next available ticket, register the start of an attendance cycle, and publish the resulting canonical call state for authorized public displays.

#### Scenario: Call next ticket
- **WHEN** an active attendant triggers the next call in the queue for their establishment
- **THEN** the system SHALL select the lowest waiting ticket, set it to called, create an attendance record, and make the resulting call and destination available to the authorized display feed.

#### Scenario: Public display reads canonical call state
- **WHEN** an authorized display requests the current call and recent call history
- **THEN** the system SHALL return the canonical current state and backend-ordered history for that display's authorized scope, and clients SHALL NOT independently select, reorder, or infer calls.

#### Scenario: No waiting ticket
- **WHEN** an active attendant requests the next call and no ticket is waiting
- **THEN** the system SHALL report that no call can be made and SHALL leave the current call state unchanged.

### Requirement: Service completion and auditability
The system SHALL complete the attendance lifecycle and persist operational events for traceability.

#### Scenario: Finish service
- **WHEN** the called ticket is completed
- **THEN** the system SHALL close the attendance, set the ticket status to completed, and log the event.

### Requirement: Queue operations baseline
The system SHALL preserve the existing queue behavior while introducing role validation, establishment isolation, and auditing as part of the delivery baseline.

#### Scenario: Baseline conservation
- **WHEN** the queue core is executed in production-like conditions
- **THEN** the system SHALL maintain consistent ordering, access control, and lifecycle status management without relying on frontend-only rules.

### Requirement: Establishment isolation
The system SHALL ensure that attendants and their operations remain isolated to the proper establishment and queue scope.

#### Scenario: Cross-establishment access attempt
- **WHEN** an attendant attempts to operate on a queue outside their establishment
- **THEN** the system SHALL deny access and leave the queue unchanged.


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
