## Why

Provisionar o Xano manualmente torna a configuração inicial suscetível a erros de dependência e dificulta repetir testes com usuários e filas previsíveis. Esta change define uma sequência verificável de importação, configuração local sem segredos versionados e um fluxo idempotente de carga de dados exclusivamente para ambientes de teste.

## What Changes

- Documentar a ordem de importação dos exports de `xano/`, separando schema, grupos, funções e endpoints, e identificar exports de exemplo ou referências ainda não resolvidas que não devem ser importados sem correção.
- Fornecer um modelo de `.streamlit/secrets.toml` alinhado às integrações Xano já consumidas pelo aplicativo, sem valores reais de credenciais.
- Criar utilitário de provisionamento repetível para Matriz, administrador, dois atendentes, serviços/filas de exemplo e credenciais de Totem e display, com autorização explícita, validação de ambiente e prevenção de duplicatas.
- Incluir testes de contrato para a ordem/imports, payloads, relações e proteção das credenciais do utilitário.
- Restringir a carga de credenciais previsíveis a workspace não produtivo; não publicar endpoints nem acessar um Xano remoto nesta change.

## Capabilities

### New Capabilities
- `xano-test-provisioning`: define o comportamento verificável do fluxo de provisionamento e dos dados sintéticos usados em ambientes de teste.

### Modified Capabilities

## Impact

- Xano: dependências e ordem dos exports sob `xano/`; provável endpoint de bootstrap de teste protegido e limitado a ambiente não produtivo, além do endpoint de registro de display já existente.
- Streamlit: `.streamlit/secrets.toml.example` e configuração local documentada; o arquivo `.streamlit/secrets.toml` real permanece ignorado pelo Git.
- Ferramentas e testes: novo utilitário Python e testes mockados de contrato; nenhuma dependência externa deve ser necessária para os testes.
- Premissas: `openspec/` contém os artefatos OpenSpec; os exports Xano a provisionar estão em `xano/`. O usuário `admin@filasmart.com` e a senha `senha123` são dados descartáveis apenas para workspace não produtivo. Credenciais de TV e Totem devem ser geradas pelo backend, armazenadas localmente fora do repositório e nunca impressas em logs.
- Fora de escopo: executar imports no painel Xano, configurar secrets reais, publicar endpoints, criar dados em workspace remoto ou usar estes usuários em produção.
