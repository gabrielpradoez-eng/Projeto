## ADDED Requirements

### Requirement: Revogação reconhece rastreamento ativo vazio
O sistema MUST revogar referências ativas ao concluir um atendimento, inclusive quando a ausência de revogação estiver armazenada como zero.

#### Scenario: Revogação reconhece rastreamento ativo vazio
- **WHEN** uma senha com referência ativa chega ao estado concluído
- **THEN** a revogação é persistida e a consulta posterior da referência é recusada.
