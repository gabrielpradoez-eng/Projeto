## Purpose

Esta capability reúne as interfaces do FilaSmart em uma experiência Streamlit centralizada, preservando os fluxos existentes, os limites de autorização e o estado necessário durante a navegação entre visões.

## ADDED Requirements

### Requirement: Central navigation exposes the available application views
O sistema SHALL oferecer uma navegação central para as visões operacionais, públicas e administrativas disponíveis, exibindo somente as opções compatíveis com o perfil autenticado ou com a configuração autorizada da interface.

#### Scenario: Usuário navega entre visões permitidas
- **WHEN** o usuário seleciona Totem, acompanhamento, Painel TV ou uma visão administrativa disponível
- **THEN** o sistema SHALL apresentar a visão selecionada dentro da aplicação central sem exigir que o usuário abra uma aplicação Streamlit distinta.

#### Scenario: Visão administrativa exige autenticação e autorização
- **WHEN** um usuário não autenticado ou sem papel administrativo tenta abrir uma visão administrativa
- **THEN** o sistema SHALL solicitar autenticação ou negar o acesso conforme o papel, sem apresentar dados administrativos.

#### Scenario: Opção de navegação não configurada
- **WHEN** uma visão depende de configuração de integração ausente ou inválida
- **THEN** o sistema SHALL informar que a visão está indisponível e SHALL manter as demais visões configuradas acessíveis.

### Requirement: Navigation preserves shared session state without mixing credentials
O sistema SHALL preservar durante a navegação o estado autenticado, o estabelecimento selecionado e as seleções de fila pertinentes, mantendo separados tokens e credenciais que pertençam a integrações ou escopos distintos.

#### Scenario: Alternar entre visões durante uma sessão
- **WHEN** um usuário autenticado navega para outra visão e retorna
- **THEN** o sistema SHALL manter a identidade e os tokens válidos, o estabelecimento autorizado e as seleções de fila ainda válidas sem exigir novo login apenas por causa da navegação.

#### Scenario: Visões usam credenciais de escopos diferentes
- **WHEN** as visões de administração, Totem e display utilizam credenciais ou tokens distintos
- **THEN** o sistema SHALL enviar cada credencial somente à integração correspondente e SHALL NOT reutilizar um token de uma visão como autorização de outra.

#### Scenario: Inicia nova sessão compartilhada do Totem
- **WHEN** uma nova sessão de emissão é iniciada no Totem
- **THEN** o sistema SHALL descartar a referência de acompanhamento e o resultado anterior do cliente antes de aceitar nova interação.

#### Scenario: Token inválido ou expirado
- **WHEN** o backend rejeita um token durante uma solicitação protegida
- **THEN** o sistema SHALL invalidar ou renovar a autenticação conforme o fluxo existente e SHALL informar a necessidade de autenticação sem preservar acesso administrativo não autorizado.

### Requirement: Centralized views preserve existing backend contracts and access boundaries
O sistema SHALL preservar as rotas, métodos, parâmetros, payloads e regras de autorização existentes para login, operações do Totem, feed do Painel TV e relatórios, sem transferir regras de negócio ou autorização para a navegação cliente.

#### Scenario: Fluxo de autenticação permanece compatível
- **WHEN** um usuário envia credenciais válidas pela visão de login
- **THEN** a aplicação SHALL consumir o contrato de autenticação existente do Xano e SHALL armazenar a identidade e a sessão retornadas sem alterar o payload exigido.

#### Scenario: Totem e acompanhamento mantêm seus contratos
- **WHEN** um cliente lista filas, emite uma senha ou consulta uma referência de acompanhamento
- **THEN** a aplicação SHALL usar os contratos existentes e SHALL exibir somente resultados confirmados pelo backend.

#### Scenario: Display e relatório mantêm seus escopos
- **WHEN** uma visão consulta o feed público ou dados analíticos
- **THEN** a aplicação SHALL usar a credencial e os filtros autorizados próprios do fluxo e SHALL NOT ampliar o escopo a partir de seleções feitas apenas no cliente.

### Requirement: API requests provide explicit and consistent visual feedback
O sistema SHALL comunicar carregamento, sucesso confirmado, ausência de dados, indisponibilidade de configuração e falha de integração sem apresentar dados simulados ou tratar falhas como sucesso.

#### Scenario: Solicitação em andamento
- **WHEN** uma visão inicia uma solicitação à API
- **THEN** a interface SHALL indicar visualmente que a solicitação está em andamento e evitar sugerir que a operação já foi concluída.

#### Scenario: Resposta válida sem resultados
- **WHEN** a API retorna uma resposta válida sem filas, chamadas ou métricas para apresentar
- **THEN** a interface SHALL mostrar um estado vazio adequado ao fluxo sem criar resultados fictícios.

#### Scenario: Solicitação falha ou backend indisponível
- **WHEN** uma solicitação falha, expira ou não pode ser realizada por falta de configuração
- **THEN** a interface SHALL indicar que os dados não foram atualizados ou que o serviço está indisponível e SHALL NOT apresentar uma resposta de sucesso nem substituir dados confirmados por dados inventados.

#### Scenario: Solicitação concluída
- **WHEN** a API confirma com sucesso uma operação ou consulta
- **THEN** a interface SHALL apresentar o resultado confirmado e uma indicação de sucesso somente quando aplicável ao fluxo.
