## ADDED Requirements

### Requirement: Credenciais de bootstrap fora da interface
O sistema MUST manter credenciais de bootstrap fora de formulários públicos.

#### Scenario: Credenciais de bootstrap fora da interface
- **WHEN** a tela de login é aberta sem sessão
- **THEN** os campos de credenciais permanecem vazios mesmo quando existe configuração de seed.

### Requirement: Provisionamento de display limitado ao estabelecimento
O sistema MUST restringir o provisionamento de displays ao estabelecimento autorizado do administrador.

#### Scenario: Provisionamento de display limitado ao estabelecimento
- **WHEN** um administrador restrito solicita display para outra unidade
- **THEN** o backend rejeita a solicitação antes de criar a credencial.
