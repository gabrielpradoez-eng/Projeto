## MODIFIED Requirements

### Requirement: Central navigation exposes the available application views
O portal unificado SHALL exigir identidade verificada antes de oferecer as visões operacionais e de cliente. O menu SHALL conter somente visões autorizadas pelo perfil remoto; criar conta permanece disponível sem sessão.

#### Scenario: Usuário navega entre visões permitidas
- **WHEN** o usuário seleciona Totem, Cliente, acompanhamento, Painel TV ou uma visão administrativa disponível
- **THEN** o sistema SHALL apresentar a visão selecionada dentro da aplicação central sem exigir que o usuário abra uma aplicação Streamlit distinta.

#### Scenario: Cliente acessa visão pública sem login administrativo
- **WHEN** um cliente com identidade verificada seleciona a visão Cliente
- **THEN** o sistema SHALL permitir emissão e acompanhamento pela sessão de cliente usando os clientes server-side autorizados, sem expor credenciais Xano.

#### Scenario: Visão administrativa exige autenticação e autorização
- **WHEN** um usuário não autenticado ou sem papel administrativo tenta abrir uma visão administrativa
- **THEN** o sistema SHALL solicitar autenticação ou negar o acesso conforme o papel, sem apresentar dados administrativos.

#### Scenario: Opção de navegação não configurada
- **WHEN** uma visão depende de configuração de integração ausente ou inválida
- **THEN** o sistema SHALL informar que a visão está indisponível e SHALL manter as demais visões configuradas acessíveis.

#### Scenario: Visitante sem sessão
- **WHEN** uma pessoa sem sessão abre o portal unificado
- **THEN** a interface SHALL apresentar somente login, cadastro e orientações, sem menu operacional.

### Requirement: Navigation preserves shared session state without mixing credentials
O sistema SHALL preservar a identidade e seleções ainda autorizadas durante a navegação, reutilizando a sessão verificada nos relatórios administrativos e mantendo separadas as credenciais técnicas de Totem e display.

#### Scenario: Alternar entre visões durante uma sessão
- **WHEN** um usuário autenticado navega para outra visão e retorna
- **THEN** o sistema SHALL manter a identidade e os tokens válidos, o estabelecimento autorizado e as seleções de fila ainda válidas sem exigir novo login apenas por causa da navegação.

#### Scenario: Visões usam credenciais de escopos diferentes
- **WHEN** as visões de administração, Totem e display utilizam credenciais ou tokens distintos
- **THEN** o sistema SHALL enviar cada credencial somente à integração correspondente e SHALL NOT usar credencial técnica como sessão administrativa; relatórios SHALL reutilizar o token administrativo verificado.

#### Scenario: Inicia nova sessão compartilhada do Totem
- **WHEN** uma nova sessão de emissão é iniciada no Totem
- **THEN** o sistema SHALL descartar a referência de acompanhamento e o resultado anterior do cliente antes de aceitar nova interação.

#### Scenario: Token inválido ou expirado
- **WHEN** o backend rejeita um token durante uma solicitação protegida
- **THEN** o sistema SHALL invalidar ou renovar a autenticação conforme o fluxo existente e SHALL informar a necessidade de autenticação sem preservar acesso administrativo não autorizado.
