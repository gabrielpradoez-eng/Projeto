## Context

Consulte [proposal.md](./proposal.md) para o problema e [specs/core-queue-ops/spec.md](./specs/core-queue-ops/spec.md) e [specs/unified-streamlit-experience/spec.md](./specs/unified-streamlit-experience/spec.md) para o comportamento exigido. A rota Live `POST /auth/login` responde com `authToken` e um objeto `user` contendo `id`, `name`, `email`, `role` e `estabelecimento_id`. O `QueueBackend.authenticate()` atual exige `user_id` no nível superior, consulta usuários em dados locais e atribui papel `admin` se a identidade remota não for localizada. A tela administrativa exibe registros locais como “usuários de exemplo”.

## Goals / Non-Goals

**Goals:**

- Tratar a resposta Live do Xano como fonte de identidade, papel e estabelecimento.
- Converter somente os papéis reconhecidos pelo contrato para os nomes já utilizados pelas visões legadas.
- Falhar explicitamente quando token, identidade ou papel estiverem ausentes ou inválidos.
- Manter token e identidade retornados pelo login ligados à mesma sessão Streamlit.

**Non-Goals:**

- Alterar ou testar credenciais reais, mudar endpoints/payload Xano ou executar login contra o Live.
- Refatorar o armazenamento em memória usado pelos demais fluxos administrativos.
- Alterar as regras de autorização no backend Xano; ele permanece a autoridade para operações protegidas.

## Decisions

### Usar o objeto `user` retornado pelo Xano

Validar `authToken` e `user` da resposta. Derivar o identificador do campo `user.id`, exigir os demais campos necessários e mapear `estabelecimento_id` para a chave interna `establishment_id`. O campo `user_id` legado retornado por `authenticate()` pode continuar existindo para compatibilidade interna, mas será derivado do ID validado do backend, não exigido como campo duplicado na resposta.

**Alternativas consideradas:** alterar a rota Xano para duplicar `user_id` no topo criaria redundância e esconderia o desacordo no cliente; aceitar apenas o payload antigo manteria o login atual quebrado.

### Normalizar papéis em uma fronteira única e fechar por padrão

Converter `admin` para `admin`, `atendente` para `attendant` e `usuario` para `user`, que são os valores consumidos pela interface existente. Rejeitar papel desconhecido, incluindo papel incompatível com a visão administrativa, em vez de escolher um perfil local.

**Alternativas consideradas:** mudar todas as visões legadas para nomes de papéis do domínio aumentaria o escopo; inferir papel pelo e-mail ou por dados locais é inseguro.

### Remover o fallback de identidade local da autenticação

Não consultar o dicionário local de usuários para decidir nome, papel ou estabelecimento após login remoto; rejeitar respostas que não contenham uma identidade válida. Remover da tela os “usuários de exemplo” que podem ser confundidos com contas reais.

**Alternativas consideradas:** manter fallback para compatibilidade transforma ausência de dados remotos em sessão local e pode conceder privilégio administrativo indevido.

## Risks / Trade-offs

- [O Xano pode alterar o formato do objeto `user`] → validar os campos necessários, retornar erro explícito e cobrir o contrato com testes unitários.
- [Os papéis `totem` não são aceitos pela visão administrativa legada] → rejeitar esse papel nessa visão; os fluxos dedicados de Totem continuam usando o cliente server-side próprio.
- [O login remoto registra evento de auditoria] → não usar contas ou chamadas ao Live em testes; usar respostas simuladas nos testes automatizados.

## Migration Plan

1. Atualizar o adaptador Streamlit para validar e normalizar o contrato Live.
2. Atualizar a sessão da visão administrativa e remover a apresentação de contas de exemplo.
3. Adicionar testes para sucesso, papéis, identidade, escopo e respostas inválidas; executar a suíte direcionada.
4. Não é necessária migração de dados nem publicação Xano. Para distribuir a correção, publicar o app Streamlit após revisão.

Rollback: reverter somente a adaptação do cliente Streamlit; o contrato Xano não muda.
