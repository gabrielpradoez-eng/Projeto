## MODIFIED Requirements

### Requirement: Central navigation exposes the available application views
O sistema SHALL oferecer uma navegação central para as visões operacionais, públicas e administrativas disponíveis, incluindo uma visão pública de Cliente acessível sem login administrativo, e SHALL exibir opções administrativas somente conforme o perfil autenticado ou configuração autorizada da interface.

#### Scenario: Usuário navega entre visões permitidas
- **WHEN** o usuário seleciona Totem, Cliente, acompanhamento, Painel TV ou uma visão administrativa disponível
- **THEN** o sistema SHALL apresentar a visão selecionada dentro da aplicação central sem exigir que o usuário abra uma aplicação Streamlit distinta.

#### Scenario: Cliente acessa visão pública sem login administrativo
- **WHEN** um cliente não autenticado administrativamente seleciona a visão Cliente
- **THEN** o sistema SHALL permitir o fluxo público de emissão e acompanhamento usando os clientes server-side autorizados, sem expor credenciais Xano.

#### Scenario: Visão administrativa exige autenticação e autorização
- **WHEN** um usuário não autenticado ou sem papel administrativo tenta abrir uma visão administrativa
- **THEN** o sistema SHALL solicitar autenticação ou negar o acesso conforme o papel, sem apresentar dados administrativos.

#### Scenario: Opção de navegação não configurada
- **WHEN** uma visão depende de configuração de integração ausente ou inválida
- **THEN** o sistema SHALL informar que a visão está indisponível e SHALL manter as demais visões configuradas acessíveis.
