## Why
Concluir os testes positivos com identidades técnicas e display aprovados pelo usuário, sem divulgar credenciais. A revogação precisa reconhecer timestamps opcionais vazios como zero, conforme observado no runtime.

## What Changes
Validar catálogo Totem, emissão, posição, chamada, feed de TV, encerramento e revogação. Incluir revogada_at=0 na seleção de rastreamentos ativos durante a finalização.

## Impact
Export de finalização, testes de regressão e registros de validação. As credenciais de teste permanecem fora do código e da documentação pública.
