## Context

See `proposal.md` for motivation and `specs/xano-test-provisioning/spec.md` for the behavior contract. The repository contains 41 `.xs` exports under `xano/`; `openspec/` contains planning/specification artifacts, not Xano exports. Current application consumers use `st.secrets` for Totem, TV, and analytics settings, and `.streamlit/secrets.toml` is already ignored by Git.

The exports are not yet a directly importable bundle: several Quick Start files still reference an empty table name, signup writes role `member` although `usuarios.role` accepts `usuario`, and some auth declarations do not name the `usuarios` table. Import and seeding guidance must account for these findings rather than imply a fresh-workspace import has already been verified.

## Goals / Non-Goals

**Goals:**
- Provide a checked-in, dependency-ordered manifest for application exports and explicitly classify generic examples and workspace metadata.
- Keep application settings and one-time seed credentials separate; require a non-production target and an explicit high-entropy seed authorization.
- Add a repeatable seed API/client contract that creates relationships in dependency order and can resume after partial failure without duplicating fixtures.
- Verify requests and responses with mocks, not a live Xano workspace.

**Non-Goals:**
- Store a Xano workspace-management key or a real deployment credential in the repository or the Streamlit app.
- Use the public signup endpoint to grant administrator, attendant, or Totem roles.
- Perform imports, deployment, or seed calls against remote Xano during local implementation or CI.

## Decisions

1. **Import resolved dependencies before consumers.** Use three API group exports first, then tables in foreign-key order: `estabelecimentos`, `usuarios`, `atendentes`, `servicos`, `filas`, `senhas`, `atendimentos`, `rastreamentos_senha`, `notificacoes`, `event_log`, `tv_displays`. Import the functions `log_event` and `generate_magic_link` after their tables, then application endpoints, and the test seed endpoint last. Within the endpoint phase, import authentication endpoints first, event log next, and queue-management endpoints after all referenced tables/functions. This is preferable to alphabetical import because Xano exports reference named groups, tables, and functions.

   The checked-in application exports now replace the empty table/auth references with `usuarios`/`event_log`, add the `password_reset` user field, and align signup's default role with the schema. The reset token is stored as a SHA-256 digest and compared as a digest. Do not import `xano/addon/user.xs`, `xano/ai/agent/xano_example_agent.xs`, `xano/ai/tool/search_xano_docs.xs`, the unused role-hierarchy example `xano/function/quick_start/enforce_role.xs`, or `xano/workspace/gabriels_workspace.xs` as application components: they are generic examples or workspace metadata, not runtime prerequisites. The manifest lists each intended file and exclusion so the order can be followed exactly.

   **Import order for the current application exports** (paths relative to repository root):

   1. API groups: `xano/api/authentication/authentication.xs`; `xano/api/event_logs/event_logs.xs`; `xano/api/queue_management/queue_management.xs`.
   2. Tables: `xano/table/estabelecimentos.xs`; `xano/table/usuarios.xs`; `xano/table/atendentes.xs`; `xano/table/servicos.xs`; `xano/table/filas.xs`; `xano/table/senhas.xs`; `xano/table/atendimentos.xs`; `xano/table/rastreamentos_senha.xs`; `xano/table/notificacoes.xs`; `xano/table/event_log.xs`; `xano/table/tv_displays.xs`.
   3. Functions: `xano/function/quick_start/log_event.xs`; `xano/function/quick_start/generate_magic_link.xs` (after replacing its empty user-table reference).
   4. Authentication endpoints: `xano/api/authentication/auth/login_POST.xs`; `xano/api/authentication/auth/signup_POST.xs`; `xano/api/authentication/auth/me_GET.xs`; `xano/api/authentication/message/send_welcome_email_POST.xs`; `xano/api/authentication/reset/request_reset_link_GET.xs`; `xano/api/authentication/reset/magic_link_login_POST.xs`; `xano/api/authentication/reset/update_password_POST.xs` (all empty user/auth references must be corrected first).
   5. Event-log endpoint: `xano/api/event_logs/logs/user/my_events_GET.xs` (correct its auth and event-log table references first).
   6. Queue endpoints: `xano/api/queue_management/attendant/dashboard_GET.xs`; `xano/api/queue_management/call_next_POST.xs`; `xano/api/queue_management/complete_POST.xs`; `xano/api/queue_management/join_POST.xs`; `xano/api/queue_management/tracking_POST.xs`; `xano/api/queue_management/analytics/options_GET.xs`; `xano/api/queue_management/analytics/report_POST.xs`; `xano/api/queue_management/totem/queues_GET.xs`; `xano/api/queue_management/totem/issue_POST.xs`; `xano/api/queue_management/tv/register_POST.xs`; `xano/api/queue_management/tv/feed_POST.xs`.
   7. Test-only endpoint added by this change: `xano/api/queue_management/setup/seed_POST.xs`, after the application dependencies above.

   `stats_GET.xs` in this change now requires an authenticated admin/active attendant and enforces establishment scope. The other excluded exports are the five example/metadata paths listed above. This classifies all 41 baseline `.xs` files; the new seed endpoint is an additional export.

2. **Bootstrap through a narrowly scoped Xano endpoint.** A local Python script cannot safely create users with elevated roles through public signup, and the repo has no management endpoints for establishments, services, queues, or attendants. Add a fixed-fixture bootstrap endpoint protected by a high-entropy Xano environment secret and an explicit non-production environment flag; reject production or disabled-seed requests before writes. It creates or resumes only the named test fixture, hashes passwords through Xano's password-typed user field, and returns newly generated attendant/Totem passwords and TV credentials once. The admin's initial password comes from local seed configuration. An authorized admin call to the existing TV registration endpoint was considered, but it cannot bootstrap the first admin or all dependent records in one idempotent run.

3. **Make repeatability deterministic and conflict-safe.** Match the establishment by its exact fixture name and users by normalized email; match services/queues by their establishment/service relationship and fixture names. Reuse exact matches, create missing records, and fail on conflicting ownership or incompatible roles rather than overwriting unrelated data. The two service estimates default to 10 minutes for the synthetic fixture. A retry after partial completion resumes by those same stable keys.

4. **Separate app secrets from seed authority.** Extend only the example template with existing `[xano]`, `[tv_display]`, and `[analytics]` keys plus a `[xano_seed]` section for the seed endpoint, non-production marker, and bootstrap secret. Use placeholders only. The script reads local configuration, requires an explicit `--confirm-test-target` option, never caches or logs passwords/tokens, and prints generated attendant/Totem/TV credentials once for the operator to transfer to local secrets. The real `.streamlit/secrets.toml` remains untracked.

   The local template shape will be:

   ```toml
   [xano]
   login_url = "https://<workspace>.xano.io/api:<auth-group>/auth/login"
   queues_url = "https://<workspace>.xano.io/api:<queue-group>/totem/queues"
   issue_url = "https://<workspace>.xano.io/api:<queue-group>/totem/issue"
   tracking_url = "https://<workspace>.xano.io/api:<queue-group>/tracking"
   totem_email = "totem@filasmart.com"
   totem_password = "<configure-local-test-password>"

   [tv_display]
   feed_url = "https://<workspace>.xano.io/api:<queue-group>/tv/feed"
   credential = "<generated-once-by-xano>"

   [analytics]
   login_url = "https://<workspace>.xano.io/api:<auth-group>/auth/login"
   options_url = "https://<workspace>.xano.io/api:<queue-group>/analytics/options"
   report_url = "https://<workspace>.xano.io/api:<queue-group>/analytics/report"

   [xano_seed]
   endpoint_url = "https://<test-workspace>.xano.io/api:<queue-group>/setup/seed"
   environment = "test"
   bootstrap_secret = "<configure-out-of-band>"
   admin_password = "<local-test-only-password>"
   ```

   The shape preserves keys already read by `streamlit_xano.py`; all URL IDs and secret values above are placeholders, not valid credentials. The seed endpoint validates its own Xano-side environment and secret independently of the local `environment` label.

5. **Keep tests offline and contract-focused.** Mock the Xano HTTP boundary and assert the payload schema, dependency ordering, deterministic fixture relations, failure before network on production/missing authorization, resumable responses, and sanitized output. Existing Xano export tests remain the precedent for static export-contract assertions; a separate live smoke test is an operator action after deployment, not a local pytest test.

## Risks / Trade-offs

- [A bootstrap endpoint could grant privileged accounts if enabled in production] → Require both an explicit non-production flag and a high-entropy server-side secret; fail closed, avoid logging the secret, and document disabling the endpoint after provisioning.
- [Existing exports contain unresolved Quick Start references] → Repair and contract-test references before publishing an import order; mark excluded templates rather than silently importing them.
- [The fixed admin test password is weak] → Accept it only for a disposable non-production workspace and never place its value in tracked files.
- [A partial seed request may leave some rows created] → Make each lookup/create step idempotent and conflict-detecting so a safe retry resumes without deleting or rewriting unrelated data.
- [One-time credentials can be lost after generation] → Display them only on successful creation, never include them in logs, and document rotating/re-registering the test credential if it is not saved.

## Migration Plan

1. Correct and validate Xano export references; add the seed endpoint and its server-side test-only guard.
2. Import API groups, tables, functions, and endpoints in the checked-in manifest order into a disposable non-production workspace.
3. Configure local `.streamlit/secrets.toml` from the placeholder example and configure the seed authorization only in the Xano environment/local secret store.
4. Run mocked local tests, then invoke the seed utility with explicit target confirmation in the non-production workspace and verify the returned fixture relations.
5. Disable the seed endpoint/secret when provisioning is complete. For rollback, disable the endpoint and remove only the named fixture records from the disposable workspace; do not run destructive cleanup against unrelated data.
