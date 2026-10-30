## Why
A revisão pré-deploy encontrou credenciais de bootstrap sendo oferecidas no formulário administrativo e provisionamento de TV sem guarda de estabelecimento. Estatísticas precisam excluir timestamps vazios armazenados como zero.

## What Changes
Manter o formulário de login vazio mesmo com Secrets de seed; limitar provisionamento de display ao escopo administrativo; excluir chamadas sem timestamp positivo da média de espera.

## Impact
Streamlit, exports Xano, testes de regressão e validação autenticada sem novas credenciais nesta etapa.

## Capabilities

### Modified Capabilities
- `core-queue-ops`: proteção de bootstrap e escopo de display.
