## Why
O aplicativo publicado mostra todas as telas antes de autenticar e mantém logins separados para operação e relatórios. O usuário solicitou acesso às funcionalidades somente após verificação do login e do perfil.

## What Changes
- Entrada única com e-mail e senha existentes no Xano, sem seleção de perfil pelo navegador.
- Confirmação canônica por auth/me antes de liberar a sessão e nas navegações.
- Cliente: Cliente, Acompanhar senha, Painel TV. Atendente: Administração e Painel TV. Administrador: todas as telas.
- Reuso do token verificado nos relatórios e operações administrativas.
- Limpeza da sessão no logout/invalidação e bloqueio de fragmentos após expiração ou mudança de perfil.

## Non-goals
Não criar contas, conceder perfis, mudar permissões de APIs ou substituir o serviço de emissão do Totem já configurado. As regras de fila e escopo continuam no Xano. Os entrypoints independentes de demonstração não são rotas do aplicativo unificado publicado.
