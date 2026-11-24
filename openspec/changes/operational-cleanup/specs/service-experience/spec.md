## ADDED Requirements
### Requirement: Erros orientados à operação
O portal MUST apresentar orientação de erro sem mostrar corpo de resposta, código de depuração ou painel técnico da API, inclusive para administradores.
#### Scenario: Recusa de emissão
- **WHEN** o backend recusa uma solicitação
- **THEN** a interface apresenta a orientação da operação sem expor payload técnico.
