## Why
A operação usa cadastros fictícios em memória, mistura os grupos de autenticação e filas e não reconhece o login legado do Xano que retorna apenas token e user_id.

## What Changes
- Separar URLs de autenticação e filas.
- Consultar auth/me com token quando login não incluir o usuário.
- Substituir o painel operacional local por leitura de attendant/dashboard e ações remotas.
- Não apresentar cadastros locais como persistidos; cadastros continuam no console Xano até existir API administrativa autorizada.

## Impact
Frontend operacional, cliente HTTP, testes de contrato. Nenhuma alteração automática nos dados ou permissões do Xano.

## Capabilities

### Modified Capabilities
- `core-queue-ops`: identidade e operação remotas.
