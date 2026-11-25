## Why
HTTP 429 recorrente impede validar fluxos no plano gratuito. Clientes independentes geram rajadas sem orçamento compartilhado.
## What Changes
Coordenar tráfego HTTP por host no processo Streamlit e reduzir polling de acompanhamento para 30 segundos. Pausar novas chamadas após 429 sem repetir mutações.
## Capabilities
### Modified Capabilities
- `service-experience`: coordenação das consultas remotas.
## Impact
Portal, autenticação, chat, totem, TV, relatórios e testes de transporte.
