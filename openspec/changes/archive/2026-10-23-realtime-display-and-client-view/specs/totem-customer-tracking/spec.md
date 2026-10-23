## ADDED Requirements

### Requirement: Public client view combines ticket issuance and tracking
O sistema SHALL oferecer na aplicação central uma visão pública de Cliente que permita escolher uma fila retornada pelo backend, solicitar a emissão de senha pelo contrato autorizado do Totem e acompanhar o estado usando a referência opaca retornada, sem expor credenciais do serviço ou dados de outros clientes.

#### Scenario: Cliente consulta filas elegíveis
- **WHEN** o cliente abre a visão pública
- **THEN** a interface SHALL exibir somente as filas disponíveis retornadas pelo backend e SHALL impedir a emissão quando não houver fila elegível.

#### Scenario: Cliente emite senha
- **WHEN** o cliente confirma a emissão para uma fila elegível
- **THEN** o cliente SHALL solicitar a operação ao endpoint autorizado `POST /totem/issue` com o campo `fila_id` e SHALL exibir número e referência de acompanhamento somente após uma resposta válida do backend.

#### Scenario: Cliente acompanha a senha emitida
- **WHEN** existe uma referência válida retornada pelo backend
- **THEN** a visão SHALL consultar o contrato de acompanhamento com essa referência e apresentar o status, posição e estimativa quando disponíveis conforme a resposta do Xano.

#### Scenario: Falha de emissão ou acompanhamento
- **WHEN** o backend rejeita a emissão ou uma consulta de acompanhamento falha
- **THEN** a interface SHALL indicar a falha ou indisponibilidade, SHALL NOT afirmar que uma senha foi emitida sem confirmação e SHALL preservar apenas o último estado de acompanhamento confirmado quando aplicável.

#### Scenario: Nova sessão de cliente
- **WHEN** um novo atendimento é iniciado na visão pública
- **THEN** a interface SHALL descartar a referência, senha e resultado de acompanhamento anteriores antes de aceitar uma nova solicitação.

#### Scenario: Credenciais de serviço permanecem privadas
- **WHEN** a visão pública solicita filas, emissão ou acompanhamento
- **THEN** as credenciais e tokens de serviço SHALL permanecer no lado servidor e SHALL NOT ser exibidos ou enviados ao navegador como conteúdo de interface.
