## Purpose

Restringir a navegação às funcionalidades autorizadas pela identidade remota e pelo estado atual da sessão.

## ADDED Requirements
### Requirement: Login verificado
Antes de renderizar qualquer funcionalidade, o aplicativo publicado MUST confirmar a identidade do token por auth/me. Credenciais inválidas, token inválido ou perfil desconhecido MUST NOT liberar navegação nem chamadas de catálogo, emissão, TV ou relatórios.

#### Scenario: Identidade inválida
- **WHEN** a identidade remota não confirma a sessão ou seu perfil
- **THEN** nenhum menu protegido ou consulta de funcionalidades é liberado.

### Requirement: Menu por perfil
O menu MUST conter somente visões autorizadas pelo perfil remoto. Uma seleção antiga ou não autorizada MUST ser substituída antes de instanciar o widget. Relatórios MUST usar o token administrativo da mesma sessão, sem segundo login.

#### Scenario: Menu da identidade confirmada
- **WHEN** um usuário entra com identidade remota válida
- **THEN** apenas visões autorizadas pelo perfil são exibidas e relatórios administrativos usam a mesma sessão.

### Requirement: Fim de sessão
Logout ou invalidação MUST limpar tokens, resultados, referências de clientes e snapshots. A verificação remota MUST ocorrer em cada navegação completa e pelo menos a cada 60 segundos em fragmentos ativos. Falha temporária de verificação MUST bloquear o conteúdo sem apresentar dados como atuais.

#### Scenario: Sessão encerrada ou indisponível
- **WHEN** a sessão expira, é encerrada ou não pode ser verificada
- **THEN** o conteúdo é bloqueado e o logout limpa dados privados; fragmentos respeitam a verificação periódica.
