# Especificação da Change: Núcleo de autenticação, cadastros e fluxo operacional básico da fila

## Visão geral
Esta especificação descreve os requisitos funcionais e de negócio do núcleo inicial do FilaSmart. O foco é garantir que a base operacional da fila e a autenticação funcionem de forma consistente e segura antes de expandir para interfaces e integrações adicionais.

## Requisitos

### REQ-01 — Autenticação de usuário
O sistema deve permitir que um usuário se autentique no backend usando credenciais válidas.

Cenário principal:
- Dado um usuário cadastrado com email e senha válidos;
- Quando ele envia as credenciais para autenticação;
- Então o sistema deve devolver um identificador de sessão/autenticação válido para uso nas operações protegidas.

Critério de aceitação:
- Login falha ao receber credenciais inválidas.
- Sessão autenticada deve identificar o usuário e o papel.

### REQ-02 — Papéis de usuário
O sistema deve distinguir os papéis admin, atendente e usuario.

Cenário principal:
- Dado um usuário com papel atendente;
- Quando ele tenta realizar uma ação de atendimento;
- Então o sistema deve permitir apenas quando sua atribuição for válida para o estabelecimento e a fila.

Critério de aceitação:
- ações sem permissão devem ser bloqueadas no backend;
- papéis diferentes devem resultar em acesso distinto conforme regra de negócio.

### REQ-03 — Cadastro de estabelecimento
O sistema deve permitir o registro de estabelecimentos físicos ou unidades operacionais.

Cenário principal:
- Dado um gestor administrativo;
- Quando registra um novo estabelecimento;
- Então o sistema deve persistir os dados básicos do local e permitir que serviços e filas sejam vinculados a ele.

Critério de aceitação:
- estabelecimento deve possuir identificador único;
- nome do estabelecimento deve ser obrigatório.

### REQ-04 — Cadastro de serviço
O sistema deve permitir o cadastro de serviços vinculados a um estabelecimento.

Cenário principal:
- Dado um estabelecimento existente;
- Quando um administrador cadastra um serviço;
- Então o serviço deve ficar associado ao estabelecimento e ter tempo estimado de atendimento definido.

Critério de aceitação:
- serviço deve pertencer a um único estabelecimento;
- nome e tempo estimado devem ser válidos.

### REQ-05 — Cadastro e estado de fila
O sistema deve suportar filas em um estabelecimento e com status de operação.

Cenário principal:
- Dado um serviço vinculado a um estabelecimento;
- Quando uma fila for criada;
- Então a fila deve apontar para esse serviço e aceitar operação conforme o seu status.

Critério de aceitação:
- fila deve possuir status aberto ou fechado;
- fila deve ser sempre associada a um serviço válido.

### REQ-06 — Emissão de senha
O sistema deve permitir que um usuário emita uma nova senha para uma fila aberta.

Cenário principal:
- Dado uma fila aberta e válida;
- Quando um usuário autenticado solicita uma senha;
- Então o sistema deve gerar o próximo número disponivel e persistir a senha com status aguardando.

Critério de aceitação:
- a senha deve receber número sequencial dentro da fila;
- fila fechada deve rejeitar nova emissão;
- a senha deve conter vínculo com usuário e fila.

### REQ-07 — Chamada da próxima senha
O sistema deve permitir que o atendente chame a próxima senha disponível da fila sob sua responsabilidade.

Cenário principal:
- Dado um atendente ativo em um estabelecimento;
- Quando a fila da qual ele é responsável tiver senhas aguardando;
- Então o sistema deve selecionar a senha com menor número e atualizar o seu status para chamado.

Critério de aceitação:
- apenas atendente ativo pode chamar senha;
- atendente não pode chamar senha de fila fora do seu estabelecimento;
- não deve haver chamada de senha inexistente.

### REQ-08 — Registro do atendimento
Quando uma senha for chamada, o sistema deve registrar o início do atendimento.

Cenário principal:
- Dado uma senha chamada;
- Quando o sistema inicia o atendimento;
- Então deve criar um registro de atendimento vinculado à senha e ao atendente.

Critério de aceitação:
- cada senha chamada deve ter um registro de atendimento vivo;
- dados de início do atendimento devem ser persistidos.

### REQ-09 — Conclusão do atendimento
O sistema deve permitir que um atendimento seja finalizado e a senha passe para concluido.

Cenário principal:
- Dado uma senha em status chamado;
- Quando o atendimento é finalizado;
- Então o sistema deve registrar o fim do atendimento e atualizar a senha para concluido.

Critério de aceitação:
- senha fora de atendimento não pode ser concluida;
- data de encerramento deve ser persistida.

### REQ-10 — Auditoria de operações críticas
O sistema deve registrar ações críticas para monitoramento e diagnóstico.

Cenário principal:
- Dado uma ação de login, emissão de senha, chamada ou conclusão;
- Quando a operação ocorre;
- Então o sistema deve gravar um evento no log com identificação do usuário, ação e metadados relevantes.

Critério de aceitação:
- log deve capturar a ação principal e o contexto da operação;
- eventos importantes devem ser rastreáveis para análise posterior.

### REQ-11 — Segurança por propriedade do estabelecimento
O sistema deve garantir que atendentes e dados permaneçam isolados por estabelecimento.

Cenário principal:
- Dado um atendente pertencente a um estabelecimento;
- Quando ele tentar acessar outra fila ou outro serviço do mesmo sistema;
- Então o sistema deve bloquear o acesso.

Critério de aceitação:
- qualquer acesso fora do escopo do estabelecimento deve ser rejeitado;
- o backend deve ser a única camada validando essa regra.

## Regras de negócio adicionais
- Todas as validações sensíveis devem ocorrer no backend do Xano.
- A interface do cliente não deve decidir regras de fila, permissão ou status da senha.
- Operações críticas devem ser tratadas com consistência transacional.
- A fila deve ser a base de verdade para sequência e ordenação do atendimento.

## Critérios de entrega desta especificação
A primeira entrega será satisfatória quando os requisitos acima forem validados em ambiente de teste e o fluxo principal de fila puder ser executado sem inconsistências de regras de negócio entre clientes.

## MODIFIED Requirements

### Requirement: Queue operations baseline
The system SHALL preserve the existing queue behavior while introducing role validation, establishment isolation, and auditing as part of the delivery baseline.

#### Scenario: Baseline conservation
- **WHEN** the queue core is executed in production-like conditions
- **THEN** the system SHALL maintain consistent ordering, access control, and lifecycle status management without relying on frontend-only rules.

