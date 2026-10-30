## Context

A branch revisada tem 220 testes e três checks aprovados. Merge e runtime são verificações independentes.

## Decisions

- Integrar o PR pelo conector GitHub, protegendo a operação com SHA esperado.
- Manter main e branch de deploy com o mesmo conteúdo no fechamento.
- Usar autenticação protegida e nunca extrair tokens do navegador.
- Uma transação isolada não demonstra serialização. A documentação oficial do Xano informa record locking dentro de transações; sintaxe e efeitos precisam ser conferidos no runtime antes de alterar endpoints.
- Registrar o bloqueio de acesso real sem concluir testes dependentes.

## Verification

Conferir merge, árvores completas, versão About e validação OpenSpec. Os 220 testes e checks anteriores permanecem evidência do código; esta etapa modifica documentação, sem mudança de runtime.
