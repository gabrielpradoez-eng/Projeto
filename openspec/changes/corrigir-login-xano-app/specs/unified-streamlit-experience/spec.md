## MODIFIED Requirements

### Requirement: Centralized views preserve existing backend contracts and access boundaries
O sistema SHALL preservar as rotas, métodos, parâmetros, payloads e regras de autorização existentes para login, operações do Totem, feed do Painel TV e relatórios, sem transferir regras de negócio ou autorização para a navegação cliente.

#### Scenario: Fluxo de autenticação permanece compatível
- **WHEN** um usuário envia credenciais válidas pela visão de login e o Xano retorna `authToken` junto de um objeto `user` válido
- **THEN** a aplicação SHALL armazenar a identidade, o papel e o escopo de estabelecimento retornados pelo Xano, sem exigir um campo `user_id` duplicado no nível superior da resposta.

#### Scenario: Resposta de autenticação inválida
- **WHEN** a resposta do Xano não contém token, identidade ou papel reconhecido
- **THEN** a aplicação SHALL negar a sessão com uma mensagem explícita e SHALL NOT inferir usuário ou papel a partir de dados locais.

#### Scenario: Login não apresenta contas de exemplo como reais
- **WHEN** um usuário não autenticado abre a visão administrativa
- **THEN** a interface SHALL solicitar credenciais sem apresentar usuários locais de exemplo como contas disponíveis para autenticação.

#### Scenario: Totem e acompanhamento mantêm seus contratos
- **WHEN** um cliente lista filas, emite uma senha ou consulta uma referência de acompanhamento
- **THEN** a aplicação SHALL usar os contratos existentes e SHALL exibir somente resultados confirmados pelo backend.

#### Scenario: Display e relatório mantêm seus escopos
- **WHEN** uma visão consulta o feed público ou dados analíticos
- **THEN** a aplicação SHALL usar a credencial e os filtros autorizados próprios do fluxo e SHALL NOT ampliar o escopo a partir de seleções feitas apenas no cliente.
