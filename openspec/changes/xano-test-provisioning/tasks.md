# Progresso do Apply: 9/9 (100%)

## 1. Inventário e imports do Xano

- [x] 1.1 Criar um manifesto com a ordem exata de importação dos exports de aplicação em `xano/`, cobrindo dependências de grupos, tabelas, funções e endpoints, e classificando os exports de exemplo/metadados a excluir; verificar o manifesto contra os 41 exports originais e o novo endpoint de seed.
- [x] 1.2 Corrigir referências de tabela/autenticação vazias nos exports usados pela aplicação e alinhar signup com os papéis aceitos por `usuarios`; adicionar testes estáticos que rejeitam referências vazias e identificam endpoints que não devem ser publicados sem autorização.
- [x] 1.3 Criar endpoint de seed exclusivo para ambiente não produtivo com segredo de bootstrap, autorização fail-closed, criação em ordem de dependência e resposta de credenciais de uso único; verificar bloqueio para produção e segredo ausente/incorreto.

## 2. Utilitário e configuração local

- [x] 2.1 Implementar `scripts/seed_xano.py` para solicitar o fixture fixo Matriz, admin, dois atendentes, serviços/filas Geral e Preferencial e identidade Totem ao endpoint de seed; verificar confirmação explícita do destino e que falhas de rede/contrato não retornam sucesso parcial.
- [x] 2.2 Tornar a criação repetível por estabelecimento/nome, e-mail e relações de serviço/fila, retomando dados parciais sem duplicar nem sobrescrever registros conflitantes; verificar comportamento de primeira execução, repetição e conflito com respostas simuladas.
- [x] 2.3 Atualizar `.streamlit/secrets.toml.example` com as chaves atuais e placeholders para configuração de seed, preservando o arquivo real no `.gitignore`; verificar que o exemplo não contém credenciais utilizáveis e que saídas/logs do utilitário não revelam segredos.

## 3. Contratos e validação

- [x] 3.1 Adicionar testes unitários/contrato mockados para ordem de importação, payloads, relações, idempotência, bloqueio de produção, credenciais e ausência de chamadas de rede; verificar que os testes passam sem configuração Xano.
- [x] 3.2 Executar a suíte completa e validar change/specs OpenSpec; verificar o comando local de pytest e `openspec validate --all --json` sem regressões.
- [x] 3.3 Após a implementação local, orientar a importação dos exports e executar manualmente o provisionador em workspace Xano descartável não produtivo; verificar login dos usuários, filas do Totem e escopo do display sem habilitar seed em produção.
