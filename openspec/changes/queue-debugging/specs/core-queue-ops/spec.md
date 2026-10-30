## ADDED Requirements

### Requirement: Confirmação operacional baseada em resposta válida
O sistema MUST confirmar emissão, chamada ou conclusão somente com resposta válida do backend.

#### Scenario: Confirmação operacional baseada em resposta válida
- **WHEN** o backend retorna erro HTTP ou identidade e estado incompletos
- **THEN** a interface informa falha sem inventar um estado de sucesso.

### Requirement: Finalização restrita ao vínculo ativo
O sistema MUST limitar a finalização ao atendente ativo responsável pelo atendimento no estabelecimento autorizado.

#### Scenario: Finalização restrita ao vínculo ativo
- **WHEN** outro atendente tenta concluir o atendimento
- **THEN** o backend rejeita a ação antes de modificar a senha.

### Requirement: Auditoria de autenticação sem segredos
O sistema MUST registrar eventos de autenticação sem senhas, hashes ou tokens.

#### Scenario: Auditoria de autenticação sem segredos
- **WHEN** uma autenticação gera um evento de auditoria
- **THEN** os metadados identificam a conta sem copiar o registro com credenciais.
