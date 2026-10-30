## Why
A revisão identificou respostas HTTP não validadas, estados de senha inventados quando faltam campos, finalização sem validação do atendente no export Xano e auditoria de registros com hashes de senha.

## What Changes
- Validar respostas operacionais e apresentar erros sem corpo sensível.
- Usar número, identidade e status canônicos das senhas retornadas pelo Xano.
- Exigir atendente ativo, estabelecimento e vínculo ao atendimento para finalizar.
- Limitar metadata dos eventos de autenticação a identificadores.

## Impact
Cliente operacional, exports Xano, testes de contrato e interface. Exports precisam de validação no runtime Xano antes de publicação; testes estáticos não executam XanoScript. Concorrência de emissão/chamada precisa de teste real separado.

## Capabilities

### Modified Capabilities
- `core-queue-ops`: contratos de operações e auditoria.
