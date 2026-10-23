## Context

Ver [proposal.md](./proposal.md) para motivação e as três specs delta para os requisitos observáveis. A aplicação já centraliza as visões em `app.py`. `views/display_view.py` declara hoje um `st.fragment` com intervalo fixo de cinco segundos e guarda snapshot/evento em `st.session_state`. `views/totem_view.py` cobre emissão e acompanhamento em componentes separados; `XanoClient` mantém credenciais do Totem server-side, lista filas, emite para a URL configurada com `fila_id` e consulta tracking com a referência opaca.

## Goals / Non-Goals

**Goals:**

- Aplicar a opção de intervalo selecionada ao ciclo de atualização do fragmento TV, preservando estado entre reruns completos.
- Adicionar uma visão pública independente que componha listagem, emissão e acompanhamento a partir dos clientes existentes.
- Preservar o contrato `POST /totem/issue` com `fila_id`, a consulta de tracking com `referencia` e a separação entre credenciais server-side e dados públicos.
- Manter as visões atuais e seus entrypoints sem duplicar a lógica de cliente Xano.

**Non-Goals:**

- Criar ou alterar endpoints Xano, papéis, permissões, formato de resposta, retenção de referências ou política de expiração.
- Tornar configurável a frequência de atualização do acompanhamento do cliente; ele conserva o ciclo atual de 15 segundos salvo mudança posterior de requisito.
- Alterar o escopo, intervalo ou conteúdo do feed de chamadas além de permitir a frequência definida nesta change.

## Decisions

### Configurar o polling TV por presets e usar o ciclo periódico nativo do Streamlit

Apresentar um seletor com 3, 5, 10, 15, 30 e 60 segundos, inicializado em cinco segundos. O valor selecionado controla o `run_every` do fragmento e a alteração do widget provoca um rerun normal do app; a renderização seguinte instala o novo intervalo. Evitar um laço com `sleep` e `st.rerun` contínuo, que bloquearia a sessão e poderia multiplicar chamadas. A chave do seletor e as chaves já usadas para snapshot e evento ficam em `st.session_state`, de modo que a mudança não repete alertas nem descarta dados confirmados.

**Alternativas consideradas:** manter cinco segundos fixos não atende à configuração pedida; um loop manual com sleep/rerun aumenta consumo e disputa o ciclo do Streamlit; uma entrada arbitrária permitiria valores extremos sem benefício operacional claro.

### Compor uma visão pública de Cliente a partir do cliente Xano existente

Adicionar `views/client_view.py` e uma opção Cliente à navegação em `app.py`. A nova visão será o ponto único para selecionar uma fila, solicitar emissão por `XanoClient.issue_ticket` (configurado para `POST /totem/issue`, corpo `{"fila_id": ...}`) e, após a resposta válida, mostrar número e iniciar o acompanhamento pela referência retornada. Reutilizar `list_queues` e `track_ticket`, sem criar uma segunda implementação HTTP nem exigir login administrativo na interface.

**Alternativas consideradas:** duplicar lógica em `app.py` criaria acoplamento e chamadas repetidas; chamar o endpoint de emissão diretamente do navegador exporia a credencial Totem; reutilizar apenas a página de Totem não cria a visão pública dedicada solicitada.

### Separar estado do ciclo de cliente de autenticação administrativa

Manter a referência, senha, resultado de tracking, fila selecionada e estado do ciclo em chaves de sessão próprias do cliente; limpar os dados anteriores ao iniciar novo atendimento. O cliente Xano conserva token/credenciais internamente no servidor e a interface apresenta somente o número e os campos de acompanhamento retornados pelo backend. Falhas preservam o último resultado confirmado como desatualizado ou exibem erro sem simular emissão.

**Alternativas consideradas:** compartilhar o estado administrativo ou persistir credenciais em widgets confundiria escopos; apagar tudo em qualquer navegação interromperia acompanhamento durante reruns.

## Risks / Trade-offs

- [Alterar o fragmento ou seu intervalo pode reinicializar o feed ou emitir alerta duplicado] → manter as chaves de snapshot/evento estáveis e testar mudança de intervalo e repetição de eventos.
- [A conta Totem pode não estar autorizada para a unidade exibida] → continuar usando somente as filas do endpoint autorizado e deixar o backend validar unidade e fila; não permitir selecionar um `unit_id` arbitrário no cliente.
- [O nome configurado para URL de emissão pode apontar para outro endpoint] → validar nos testes de contrato a URL `/totem/issue`, o método POST e o corpo exato `{"fila_id": id}`.
- [A referência opaca é sensível mesmo sem identificar diretamente o cliente] → não incluí-la em logs ou mensagens públicas além do fluxo de acompanhamento já existente e limpá-la ao iniciar novo atendimento.

## Migration Plan

1. Adicionar testes de comportamento para seleção do intervalo, ciclo do feed e requisições Xano do fluxo de Cliente.
2. Parametrizar o fragmento TV sem alterar seu tratamento de snapshot, histórico, polling e alertas.
3. Criar `client_view.py` reutilizando o cliente Xano e os estados de sessão existentes para emissão/acompanhamento.
4. Incluir Cliente na navegação central e validar estados vazios, falhas, sucesso, preservação de sessão e privacidade.
5. Executar testes focados, suíte completa e `openspec validate --all`. Para rollback, remover a rota e a visão Cliente e restaurar o intervalo fixo de cinco segundos; nenhum dado ou endpoint requer migração.
