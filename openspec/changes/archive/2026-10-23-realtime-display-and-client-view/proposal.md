## Why

O Painel TV atual atualiza em intervalo fixo, sem permitir ajustar a frequência à infraestrutura ou ao contexto de exibição. Além disso, a experiência central ainda distribui emissão e acompanhamento entre telas, em vez de oferecer ao cliente uma visão pública dedicada para retirar senha e acompanhar seu estado.

## What Changes

- Permitir configurar a frequência de atualização do Painel TV com padrão de 5 segundos e opções de 3, 5, 10, 15, 30 e 60 segundos, aplicando a escolha dinamicamente sem perder o snapshot, o histórico ou o controle de alertas.
- Adicionar à navegação central uma visão pública de Cliente em `app.py`, com componente dedicado, que lista as filas autorizadas, emite senha pelo endpoint existente `POST /totem/issue` usando `fila_id` e acompanha o status pela referência opaca retornada.
- Preservar os contratos, escopos e credenciais server-side existentes do Xano; não expor credenciais do Totem na interface pública.
- Cobrir o polling configurável e o ciclo de emissão/acompanhamento com testes de regressão, incluindo estados vazios e falhas de API.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `tv-display-panel`: alterar a frequência de polling do display para permitir configuração dentro de limites definidos, mantendo atualização, alertas, snapshot e tratamento de indisponibilidade.
- `totem-customer-tracking`: especificar a visão pública de Cliente que reúne emissão pelo contrato Totem e acompanhamento pela referência opaca, mantendo as proteções de sessão e dados existentes.
- `unified-streamlit-experience`: incluir a nova visão pública de Cliente na navegação central e preservar os limites de acesso e estado do ciclo de emissão/acompanhamento.

## Impact

- Interfaces Streamlit: `app.py`, `views/display_view.py` e novo módulo planejado `views/client_view.py`; o fluxo atual em `views/totem_view.py` poderá fornecer componentes reutilizáveis.
- Clientes e contratos existentes: `/totem/queues`, `POST /totem/issue` com `fila_id` e endpoint de tracking com referência opaca; nenhuma mudança pretendida no backend Xano.
- Testes de regressão do display e da aplicação central para intervalo, navegação, emissão, acompanhamento, falhas e preservação de dados.

## Fora de escopo

- Alterar endpoints, autenticação, papel do usuário Totem, autorização de estabelecimento ou regras de fila no Xano.
- Alterar o formato do snapshot do Painel TV, o algoritmo de ordenação do backend ou o conteúdo público que ele retorna.
- Expor tokens, credenciais de serviço ou identificadores internos de clientes no navegador.
