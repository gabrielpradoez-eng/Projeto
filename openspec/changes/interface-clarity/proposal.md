## Why
Os formulários exibem seleções únicas como escolhas, conceitos de serviço/fila sem ajuda e horários técnicos. O botão de reinício aparece mesmo sem comprovante local.

## What Changes
- Explicar serviço e fila, apresentar estabelecimento único como informação e selecionar automaticamente fila única nos relatórios.
- Atualizar dependências de filtros antes da consulta, sem enviar relatório automaticamente.
- Apresentar datas legíveis com limites UTC explícitos e indicadores com linguagem comum.
- Exibir reinício apenas com senha local e corrigir a orientação de atualização para 30 segundos.

## Capabilities
### New Capabilities
- `interface-clarity`: formulários e relatórios compreensíveis, com seleções contextuais.
### Modified Capabilities
Nenhuma regra de autorização, cálculo ou janela UTC é alterada.

## Impact
Views Streamlit, testes de interface e README. Sem mudanças nos exports ou registros Xano. Fora do escopo: exclusão de dados, recuperação de senha e mudança de fuso do contrato analítico.
