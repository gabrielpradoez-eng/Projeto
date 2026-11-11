## ADDED Requirements

### Requirement: Corporate responsive portal
O portal SHALL apresentar identidade empresarial consistente e adaptar o conteúdo à largura disponível, com formulários legíveis e controles acionáveis por toque.

#### Scenario: Narrow screen
- **WHEN** a largura disponível é de até 900 pixels
- **THEN** a navegação entre áreas autorizadas e a saída ficam disponíveis no conteúdo, sem depender da abertura da barra lateral.

#### Scenario: Small phone
- **WHEN** a largura é de até 640 pixels
- **THEN** colunas de conteúdo e métricas empilham, campos mantêm texto legível e botões oferecem pelo menos 44 pixels de altura.

### Requirement: Navigation state remains authorized and consistent
As navegações de desktop e celular MUST compartilhar a área selecionada e mostrar somente opções do perfil verificado.

#### Scenario: Switch using mobile navigation
- **WHEN** o usuário seleciona outra área autorizada pelo seletor da página
- **THEN** a seleção da barra lateral acompanha a mudança e o conteúdo correto é exibido.

#### Scenario: Identity changes
- **WHEN** a sessão expira ou o perfil perde uma permissão
- **THEN** o seletor móvel não permite acesso à área anterior nem mostra conteúdo protegido sem verificação.
