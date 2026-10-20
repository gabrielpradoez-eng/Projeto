## Why

Administradores precisam acompanhar volume e desempenho dos atendimentos ao longo do tempo para identificar filas sobrecarregadas e variações de espera. Hoje o Xano expõe apenas contagens e uma média recente por fila, sem período configurável, agregações comparáveis ou uma visão administrativa; esta change define métricas consistentes no backend e uma visualização Streamlit sem cálculos de negócio no cliente.

## What Changes

- Criar relatórios administrativos com filtros de período, serviço e fila, sempre limitados ao estabelecimento autorizado.
- Disponibilizar no Xano totais de emissões, chamadas e conclusões por data do evento, distribuição do status atual dos tickets emitidos no período, tempo de espera entre emissão e chamada e duração entre início e fim do atendimento.
- Retornar séries temporais agregadas e agrupamentos por serviço/fila já calculados e ordenados pelo Xano.
- Definir denominadores e contagens de amostra para médias e taxas; períodos sem dados devem retornar agregados vazios/nulos de forma explícita.
- Criar uma interface Streamlit para filtros e visualização tabular/gráfica, apresentando fielmente os agregados recebidos sem recalcular ou reordenar métricas.
- Fora de escopo: previsões de demanda, recomendações automáticas, metas/SLA configuráveis, satisfação do cliente, dados individualizados de clientes, exportação de registros pessoais e alteração do fluxo de atendimento.

## Capabilities

### New Capabilities
- `analytics-and-reports`: consulta autorizada e visualização administrativa de métricas agregadas de filas e atendimentos, com soberania de cálculo e agregação no Xano.

### Modified Capabilities

## Impact

- Xano: novos contratos autenticados para resumo, séries temporais e agrupamentos; agregações, interpretação do período e autorização por estabelecimento permanecem no backend.
- Streamlit: nova visão administrativa para selecionar período/serviço/fila, apresentar KPIs e tendências e tratar estados sem dados/erro.
- Dados: usa `senhas.created_at`, `chamado_at`, `concluido_at`, status, e `atendimentos.started_at`/`ended_at`, associados a fila, serviço e estabelecimento.
- Premissas iniciais: período em UTC com início inclusivo e fim exclusivo; espera é `chamado_at - created_at`; duração do atendimento é `ended_at - started_at`; médias incluem somente registros com os dois timestamps necessários e retornam a quantidade de amostras. Como não há timestamp nem rota de cancelamento no modelo atual, cancelamentos serão mostrados apenas como status atual dos tickets da coorte emitida no período, não como eventos de cancelamento ocorridos naquele período. Administradores vinculados a um estabelecimento ficam restritos a ele; administradores globais precisam selecionar um estabelecimento autorizado.