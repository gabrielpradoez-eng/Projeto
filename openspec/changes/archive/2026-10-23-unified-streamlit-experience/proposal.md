## Why

As funcionalidades do FilaSmart estão distribuídas entre diferentes aplicações Streamlit, o que torna a navegação e a manutenção da sessão inconsistentes para operadores e administradores. Uma experiência centralizada facilita a descoberta das visões sem alterar a autoridade do Xano sobre autenticação, filas e métricas.

## What Changes

- Criar uma aplicação Streamlit central com navegação clara entre Totem, acompanhamento de senha, Painel TV e áreas administrativas, incluindo relatórios.
- Organizar as visões em módulos independentes e renderizar a visão selecionada sem reinicializar a sessão compartilhada.
- Preservar tokens e estados de autenticação com escopos distintos, estabelecimento selecionado e dados de interface necessários, sem ampliar permissões entre visões.
- Padronizar feedback visual para carregamento, sucesso, ausência de dados, falha e configuração indisponível nas chamadas às APIs.
- Manter os contratos e as regras de autorização existentes do Xano; atualizar os testes de regressão das visões e integrações.

## Capabilities

### New Capabilities

- `unified-streamlit-experience`: navegação centralizada entre as visões Streamlit com estado persistente, acesso compatível com cada perfil e feedback consistente de integração.

### Modified Capabilities

Nenhuma. Os contratos funcionais de filas, Totem, display e relatórios permanecem definidos pelas capabilities existentes; esta mudança especifica a experiência de navegação que as reúne.

## Impact

- Aplicação e módulos Streamlit: `app.py`, `kiosk_app.py`, `tv_display_app.py`, `analytics_app.py`, `app_pages/` e os módulos de cliente compartilhados.
- Testes das interfaces e dos contratos Xano para login, filas do Totem, feed da TV e relatórios.
- Nenhuma alteração pretendida nos endpoints, dados ou regras de negócio do Xano.

## Fora de escopo

- Alterar autenticação, papéis, permissões, regras de filas, contratos ou agregações do backend.
- Substituir Streamlit, adicionar dependências de navegação ou redesenhar individualmente cada fluxo além do necessário para integrá-lo à aplicação central.
