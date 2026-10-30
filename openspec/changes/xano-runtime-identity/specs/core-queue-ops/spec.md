## ADDED Requirements

### Requirement: Perfil de autorização lido da conta persistida
O sistema MUST determinar perfil e estabelecimento pela conta persistida correspondente ao identificador autenticado.

#### Scenario: Perfil de autorização lido da conta persistida
- **WHEN** uma operação protegida recebe um token válido
- **THEN** as permissões são lidas do banco sem depender de campos de perfil ausentes no token.

### Requirement: Consultas limitadas ao escopo operacional
O sistema MUST retornar apenas filas, serviços e indicadores pertencentes ao escopo autorizado, aceitando filtros opcionais vazios conforme o contrato.

#### Scenario: Consultas limitadas ao escopo operacional
- **WHEN** um atendente consulta filas ou um administrador gera relatório
- **THEN** o resultado preserva o isolamento e não falha por valores opcionais vazios.
