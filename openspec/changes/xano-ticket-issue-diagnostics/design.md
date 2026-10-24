## Context

Consulte [proposal.md](./proposal.md) para a motivação e a spec delta para o contrato observável. `XanoClient` já envia `POST /totem/issue` com `{"fila_id": id}` e token server-side. Atualmente, ao receber um `HTTPError`, o cliente extrai apenas `message` e descarta o corpo bruto e outros campos como `code`; as duas visões exibem somente os atributos disponíveis.

## Goals / Non-Goals

**Goals:**

- Preservar status HTTP e corpo limitado da resposta de erro em propriedades tipadas da exceção.
- Exibir os detalhes de forma consistente nas visões Totem e Cliente.
- Registrar contexto operacional sem persistir nem registrar credenciais.
- Manter intactos endpoint, payload e autenticação atuais.

**Non-Goals:**

- Alterar o contrato Xano ou incluir tokens/chaves no corpo da emissão.
- Fazer chamadas remotas reais como parte dos testes.
- Registrar corpo de erro integral sem limite.

## Decisions

### Preservar corpo e extrair campos sem perder compatibilidade

Adicionar `api_body` e `api_code` às exceções de requisição e fila. O corpo será lido uma única vez, limitado a 4096 caracteres; a extração de `message` continuará disponível para chamadas existentes. Erros sem corpo ou com codificação/JSON inválidos continuam apresentando o status e um texto seguro de fallback.

**Alternativas consideradas:** apenas exibir `message` mantém o problema atual; reler `HTTPError` depois de parsear pode falhar porque o stream já foi consumido; retornar um formato novo em vez de exceção exigiria alterar todos os chamadores.

### Diagnóstico estruturado sem segredos

Registrar método, caminho do endpoint, status e código de erro quando presentes. Excluir query string, credenciais, corpo da requisição e cabeçalhos de autorização dos logs. A interface poderá mostrar o corpo de erro limitado recebido do backend, sem qualquer token enviado pelo cliente.

**Alternativas consideradas:** logar `Request` completo poderia expor tokens; omitir qualquer log não atende à necessidade de identificar status e rota.

## Risks / Trade-offs

- [O corpo de erro pode conter texto extenso ou sensível] → limitar a 4096 caracteres, não registrar o corpo bruto e nunca registrar payload/cabeçalhos de autenticação.
- [Uma alteração no tratamento pode ocultar exceções legadas] → preservar `status_code` e `api_message`, acrescentando apenas atributos opcionais, com testes para 400, 404, corpo vazio e corpo estruturado.

## Migration Plan

1. Atualizar parsing de erro e logging no cliente Xano.
2. Propagar os detalhes nas exceções de fila e apresentá-los em ambas as visões.
3. Validar os contratos por testes unitários e de interface e executar toda a suíte.

Rollback: reverter o tratamento de corpo detalhado e manter os contratos de endpoint/payload inalterados.
