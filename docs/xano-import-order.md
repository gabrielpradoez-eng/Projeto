# Ordem de importação do Xano

Os exports Xano estão em `xano/` (não em `openspec/`). O inventário inclui os componentes da aplicação, o endpoint de seed e a rotina interna de apresentação, totalizando 43 arquivos classificados. Importe somente em um workspace descartável/não produtivo depois de corrigir as referências indicadas abaixo.

## Pré-requisitos antes do primeiro import

1. Configure a tabela `usuarios` como tabela de autenticação e mantenha seus papéis conforme o schema.
2. Faça os reparos apontados em “Correções necessárias”. Não importe exports ainda com referências vazias.
3. O `stats_GET.xs` desta change exige autenticação e valida papel/estabelecimento; não substitua por uma versão pública antiga.
4. Confirme que as URLs e IDs de API Group no workspace de destino correspondem aos consumers do Streamlit; este manifesto não publica nem configura o workspace.
5. No Xano, configure `xano_environment=test`, `seed_enabled=true` e `seed_secret` com valor aleatório de alta entropia. Mantenha seed desabilitado fora do provisionamento e remova/desabilite o endpoint após a carga.

## Sequência

### 1. Grupos de API

1. `xano/api/authentication/authentication.xs`
2. `xano/api/event_logs/event_logs.xs`
3. `xano/api/queue_management/queue_management.xs`

### 2. Tabelas

Importe as tabelas referenciadas por chaves estrangeiras antes das tabelas dependentes:

1. `xano/table/estabelecimentos.xs`
2. `xano/table/usuarios.xs`
3. `xano/table/atendentes.xs`
4. `xano/table/servicos.xs`
5. `xano/table/filas.xs`
6. `xano/table/senhas.xs`
7. `xano/table/atendimentos.xs`
8. `xano/table/rastreamentos_senha.xs`
9. `xano/table/notificacoes.xs`
10. `xano/table/event_log.xs`
11. `xano/table/tv_displays.xs`

### 3. Funções compartilhadas

1. `xano/function/quick_start/log_event.xs`
2. `xano/function/quick_start/generate_magic_link.xs`

### 4. Endpoints de autenticação

1. `xano/api/authentication/auth/login_POST.xs`
2. `xano/api/authentication/auth/signup_POST.xs`
3. `xano/api/authentication/auth/me_GET.xs`
4. `xano/api/authentication/message/send_welcome_email_POST.xs`
5. `xano/api/authentication/reset/request_reset_link_GET.xs`
6. `xano/api/authentication/reset/magic_link_login_POST.xs`
7. `xano/api/authentication/reset/update_password_POST.xs`

### 5. Endpoint de logs

1. `xano/api/event_logs/logs/user/my_events_GET.xs`

### 6. Endpoints de filas, Totem, display e analytics

1. `xano/api/queue_management/attendant/dashboard_GET.xs`
2. `xano/api/queue_management/call_next_POST.xs`
3. `xano/api/queue_management/complete_POST.xs`
4. `xano/api/queue_management/join_POST.xs`
5. `xano/api/queue_management/stats_GET.xs` — somente após confirmar as restrições de autenticação e estabelecimento.
6. `xano/api/queue_management/tracking_POST.xs`
7. `xano/api/queue_management/analytics/options_GET.xs`
8. `xano/api/queue_management/analytics/report_POST.xs`
9. `xano/api/queue_management/totem/queues_GET.xs`
10. `xano/api/queue_management/totem/issue_POST.xs`
11. `xano/api/queue_management/tv/register_POST.xs`
12. `xano/api/queue_management/tv/feed_POST.xs`

### 7. Seed de teste

Importe `xano/api/queue_management/setup/seed_POST.xs` somente depois dos grupos, tabelas, funções e endpoints de que depende, e somente em workspace de teste com a proteção de seed habilitada.

### 8. Rotina manual de apresentação

`xano/function/prepare_presentation.xs` é uma função interna, sem endpoint público, para o cenário de demonstração identificado no próprio código. Não é uma dependência da aplicação. O padrão `apply=false` apenas consulta; `apply=true` prepara os dados em transação, sem criar credenciais ou excluir registros. Confira os IDs e as precondições antes de reutilizar em outro workspace. Chaves determinísticas de evento impedem duplicar o histórico ao repetir a execução.

## Correções necessárias nos exports

- As referências vazias a tabelas nos exports de autenticação devem apontar para `usuarios`; o endpoint pessoal de logs usa `event_log`. Os exports de `generate_magic_link` e `log_event` também precisam usar as tabelas nomeadas correspondentes.
- O endpoint de signup deve criar papel `usuario`, aceito pelo enum de `usuarios`, e não `member`.
- `me_GET`, `update_password_POST` e `my_events_GET` devem usar autenticação `usuarios`.
- O endpoint de envio de boas-vindas deve autenticar o chamador e limitar envio ao próprio usuário ou a um administrador.
- A tabela `usuarios` precisa comportar os dados de reset (`password_reset`) usados pelos exports de redefinição.
- `stats_GET` deve exigir autenticação e validar papel e estabelecimento antes de consultar contagens. Não disponibilize a versão pública/sem escopo.
- O seed é uma API exclusiva de ambiente não produtivo e sua autorização deve ser configurada no Xano fora do código exportado. A chamada usa HTTPS; restrinja também o acesso aos registros de execução do workspace enquanto o endpoint estiver habilitado.

## Arquivos fora da sequência de aplicação

Os cinco arquivos seguintes são exemplos genéricos ou metadados e não são dependências da aplicação:

- `xano/addon/user.xs` — addon Quick Start com tabela vazia `user`.
- `xano/ai/agent/xano_example_agent.xs` — agente de exemplo.
- `xano/ai/tool/search_xano_docs.xs` — ferramenta de exemplo.
- `xano/function/quick_start/enforce_role.xs` — exemplo de hierarquia de papéis incompatível com o enum atual.
- `xano/workspace/gabriels_workspace.xs` — preferências/metadata de workspace, não componente da API.

O inventário base contém 41 exports: 36 componentes de aplicação na sequência principal e cinco exemplos/metadata excluídos. Com o endpoint de seed e a rotina manual de apresentação, o inventário atual contém 43 arquivos classificados.
