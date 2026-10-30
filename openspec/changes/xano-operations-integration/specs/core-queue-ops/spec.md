## ADDED Requirements

### Requirement: Login legado confirmado pela identidade remota
O sistema MUST confirmar a identidade por auth/me quando o login retornar somente token e identificador.

#### Scenario: Login legado confirmado pela identidade remota
- **WHEN** o serviço de login retorna authToken e user_id sem objeto de usuário
- **THEN** o cliente consulta a identidade remota e rejeita identificação incompatível.

### Requirement: Painel operacional persistido no backend
O sistema MUST apresentar filas e atendimentos autorizados retornados pelo backend.

#### Scenario: Painel operacional persistido no backend
- **WHEN** o atendente atualiza seu painel
- **THEN** os dados vêm da operação remota e cadastros locais não são apresentados como persistidos.
