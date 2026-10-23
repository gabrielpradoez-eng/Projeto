## Context

Ver [proposal.md](./proposal.md) para a motivação e [spec.md](./specs/unified-streamlit-experience/spec.md) para os contratos observáveis. Atualmente, `app.py`, `kiosk_app.py`, `tv_display_app.py` e `analytics_app.py` são entradas Streamlit separadas; há páginas do Totem/acompanhamento em `app_pages/`, clientes Xano compartilhados em `streamlit_xano.py` e testes específicos por fluxo. O display também mantém atualização periódica e estado próprio, enquanto Analytics tem autenticação distinta.

## Goals / Non-Goals

**Goals:**

- Tornar `app.py` a entrada de uma aplicação com navegação central e execução apenas da visão ativa.
- Extrair as interfaces em módulos de visão reutilizáveis, mantendo chamadas e regras de autorização nos clientes Xano e no backend.
- Preservar os estados existentes que são válidos entre reruns e navegações, sem combinar tokens de autenticação com credenciais de Totem, display ou Analytics.
- Adicionar testes de regressão para navegação, persistência de estado, restrições por perfil, estados de API e contratos dos clientes.

**Non-Goals:**

- Alterar endpoints, payloads, regras de negócio, dados ou permissões no Xano.
- Fazer uma reimplementação visual completa de cada fluxo ou introduzir um novo framework/dependência de interface.

## Decisions

### Usar uma entrada Streamlit central e navegação lateral nativa

`app.py` será responsável por configurar a aplicação, inicializar somente valores ausentes de `st.session_state`, resolver autenticação/perfil e encaminhar a execução para a visão ativa. A navegação lateral nativa do Streamlit é preferida a duplicar visões em abas: somente a rota selecionada será renderizada, evitando disparar chamadas de todas as APIs a cada rerun e reduzindo conflitos entre componentes com estado próprio.

**Alternativas consideradas:** `st.tabs` simplificaria a navegação, mas pode executar o conteúdo de várias abas no mesmo ciclo; manter os aplicativos separados não resolve a experiência fragmentada.

### Extrair as visões em módulos reutilizáveis

As responsabilidades visuais serão movidas para módulos sob `views/` (Admin, Totem, acompanhamento, Display e Analytics, conforme os fluxos identificados). A camada de navegação seleciona e chama a visão; clientes existentes, como `streamlit_xano.py`, continuam responsáveis por construir integrações. Os arquivos de entrada atuais poderão ser reduzidos a adaptadores para preservar comandos/configurações de execução existentes durante a migração, sem manter implementações de UI duplicadas.

**Alternativas consideradas:** reescrever tudo em um único `app.py` preservaria menos fronteiras de responsabilidade; criar novas fábricas de API duplicaria os clientes já existentes.

### Manter identidades e tokens em namespaces separados

Inicializar e preservar o estado global sem sobrescrever valores já existentes entre reruns. A autenticação principal, o token de Analytics e as credenciais de Totem/Display continuam isolados por fluxo e serão passados somente ao cliente correspondente. Seleção de estabelecimento e filas deve permanecer no escopo autorizado do usuário e ser validada novamente pelos contratos atuais do backend. Uma nova sessão do Totem continua limpando a referência e o resultado do cliente anterior, conforme a spec existente.

**Alternativas consideradas:** um token ou objeto de sessão único reduziria estado, mas poderia enviar credenciais a um endpoint incorreto e misturar permissões; limpar todo o estado a cada navegação causaria logins repetidos e perda de contexto.

### Preservar a atualização do Display somente quando sua visão estiver ativa

Manter o polling, o snapshot, os alertas e a ordem fornecida pelo backend existentes, mas renderizar o fragmento periódico dentro da visão Display. Assim a navegação para outras áreas não mantém chamadas periódicas desnecessárias nem altera o comportamento enquanto o painel está aberto.

**Alternativas consideradas:** polling global na aplicação central consumiria recursos mesmo fora do Display; remover o fragmento degradaria a atualização já existente.

### Padronizar feedback sem mascarar falhas

As visões devem usar os padrões Streamlit de carregamento, sucesso, vazio e erro junto às chamadas existentes. Mensagens de erro permanecem explícitas, e respostas antigas ou vazias não devem ser transformadas em sucesso ou em dados simulados. Não adicionar um mecanismo global de retentativa ou cache sem necessidade demonstrada pelos fluxos atuais.

## Risks / Trade-offs

- [A mudança de chaves/widget state pode perder estado salvo ou causar colisões] → preservar chaves existentes quando compatível, prefixar novas chaves por visão e cobrir navegação em testes.
- [A navegação pode expor uma visão a um perfil indevido se tratada como autorização] → usar perfil/configuração apenas para controlar a apresentação; manter todas as decisões de acesso nos fluxos e validações do backend.
- [A extração pode quebrar comandos de execução usados por implantação ou testes] → manter adaptadores de entrada durante a migração e validar as entradas centrais e legadas na suíte.
- [Polling/fragmento do Display pode interferir nos reruns da aplicação] → renderizar e testar o fragmento apenas quando a visão correspondente estiver selecionada.

## Migration Plan

1. Extrair primeiro funções e componentes existentes para módulos de visão, sem mudar contratos Xano.
2. Implementar o shell central em `app.py` e conectar as visões com inicialização de sessão e controles de acesso preservados.
3. Adaptar as entradas antigas como delegadores temporários, quando necessário, para manter os comandos de execução existentes.
4. Executar testes focados por fluxo e, em seguida, a suíte completa; corrigir incompatibilidades antes de alterar a entrada recomendada de execução.
5. Para rollback, reverter a seleção da entrada central e voltar aos entrypoints anteriores enquanto preservadas as chamadas Xano; não é necessária migração de dados.
