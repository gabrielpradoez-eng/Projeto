## Context

Consulte proposal.md. O AnalyticsClient verificava somente dict/list; as views indexam IDs e campos numéricos. A mudança de escopo pode manter seleções e relatório da navegação anterior.

## Goals / Non-Goals

Validar os campos usados na apresentação e preservar apenas relatórios compatíveis com o catálogo atual. Não recalcular métricas, ordenar dados analíticos ou modificar endpoints Xano.

## Decisions

- Validadores no cliente HTTP rejeitam IDs inválidos/duplicados, vínculos de opções fora do catálogo e formas/valores inválidos em relatórios.
- A view compara assinatura canônica do catálogo (independente da ordem), redefine estabelecimento/serviço antes dos widgets e limpa o relatório quando a assinatura muda ou as opções falham.
- Manter suporte a timestamps UTC numéricos e ISO, usados pelo Xano, e a médias nulas sem amostras.
- Registrar relatório de auditoria com evidências de CI, branch e main. Corrigir documentação e checklists somente com evidência já observada ou obtida nesta revisão.
- CI Python complementa o workflow OpenSpec existente. Nenhum secret é necessário nos testes.

## Risks / Trade-offs

Mudanças no contrato remoto passam a ser recusadas explicitamente → documentar o contrato e testar o formato numérico real do Xano.
Checklists históricos podem ter sido superados → citar a evidência posterior e preservar concorrência e cadastro positivo como pendências.
