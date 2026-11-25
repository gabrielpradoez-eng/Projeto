## Context
O backend mantém identidades, escopos e cálculos. A alteração é de apresentação e interação.

## Goals / Non-Goals
Simplificar escolhas sem alterar IDs autorizados, métricas ou fim exclusivo UTC. Não criar regras de negócio no cliente.

## Decisions
- Reutilizar um controle que apresenta uma opção como texto e mantém seleção com múltiplas opções.
- Filtros analíticos fora de formulário atualizam serviço/fila na mesma interação. O botão Gerar relatório continua obrigatório para a consulta agregada.
- A fila única só é automática quando um serviço específico está selecionado; com todos os serviços, manter todas as filas.
- Horários de limites permanecem UTC; geração usa São Paulo. Rótulos de gráfico/tabela mudam sem recalcular ou reordenar agregados.
- Reinício depende da referência local, preservando comprovante e ausência de cancelamento.

## Risks / Trade-offs
Mudanças de filtros provocam rerun, mas não consulta de métricas. Validar troca entre opções únicas/múltiplas e remoção de seleção para impedir IDs antigos.

## Validation
Testes AppTest com respostas controladas, suíte Python, OpenSpec estrito e conferência do deploy. Não usar dados simulados como evidência do Xano.
