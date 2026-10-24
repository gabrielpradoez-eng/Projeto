## ADDED Requirements

### Requirement: Ticket issuance errors provide actionable Xano diagnostics
Quando o Xano rejeita uma solicitação de emissão de senha, a interface SHALL apresentar o status HTTP e o corpo de erro retornado pelo backend, incluindo o código ou a mensagem de validação quando disponíveis, sem revelar credenciais ou cabeçalhos de autorização.

#### Scenario: Backend retorna erro estruturado na emissão
- **WHEN** uma solicitação de emissão é rejeitada com status HTTP e corpo JSON de erro
- **THEN** a interface SHALL exibir o status e os detalhes retornados pelo Xano para orientar a correção da solicitação.

#### Scenario: Backend retorna erro sem corpo JSON legível
- **WHEN** uma solicitação de emissão é rejeitada e o corpo não é JSON válido ou está vazio
- **THEN** a interface SHALL exibir o status HTTP e o corpo legível disponível, ou indicar que o backend não forneceu detalhes adicionais.

#### Scenario: Diagnóstico é registrado sem credenciais
- **WHEN** uma falha HTTP de emissão é registrada para diagnóstico
- **THEN** o registro SHALL identificar método, endpoint e status e SHALL NOT incluir senha, token ou cabeçalho de autorização.
