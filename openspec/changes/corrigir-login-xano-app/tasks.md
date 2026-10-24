## 1. Adaptar autenticação ao contrato Live

- [x] 1.1 Atualizar o cliente administrativo para validar `authToken` e o objeto `user` retornados pelo Xano, derivar o ID e estabelecimento da resposta e normalizar `admin`, `atendente` e `usuario`; verificar com testes unitários do contrato real.
- [x] 1.2 Rejeitar token, identidade ou papel ausente/desconhecido sem usar perfil local como fallback; verificar com testes negativos incluindo usuário remoto não presente nos dados em memória.

## 2. Corrigir a experiência de login

- [x] 2.1 Remover a lista de usuários de exemplo da tela sem login e validar via `AppTest` que a interface solicita credenciais sem sugerir contas fictícias.
- [x] 2.2 Executar os testes direcionados de autenticação e interface e confirmar que os fluxos administrativos aceitam os papéis mapeados e que respostas inválidas não criam sessão.
