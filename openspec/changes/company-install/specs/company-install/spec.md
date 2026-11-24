## Purpose
Permitir que cada empresa configure sua instalação independente e seu catálogo operacional.
## ADDED Requirements
### Requirement: Catálogo administrativo
O sistema MUST permitir somente ao administrador criar ou editar nome do serviço, duração estimada, nome e estado da fila dentro do estabelecimento autorizado, sem excluir histórico nem mudar o estabelecimento na edição.
#### Scenario: Cadastro
- **WHEN** o administrador envia dados válidos no seu escopo
- **THEN** serviço e fila são persistidos na mesma transação.
#### Scenario: Acesso indevido
- **WHEN** uma conta sem perfil administrativo ou fora do escopo tenta alterar o catálogo
- **THEN** a operação é rejeitada sem alterações.
### Requirement: Instalação identificável
O portal MUST permitir nome e cor por configuração, validando cor e escapando texto usado em HTML.
#### Scenario: Configuração ausente
- **WHEN** não há identificação de empresa configurada
- **THEN** a marca padrão FilaSmart continua disponível.
### Requirement: Ativação controlada
O catálogo MUST ficar oculto até ativação explícita após implantação do backend.
#### Scenario: Backend ainda não publicado
- **WHEN** a flag de catálogo não está ativa
- **THEN** o portal não oferece alterações do catálogo.
