## Why
Teste autenticado no runtime Xano retornou ERROR_FATAL: Unable to locate auth: role. O contexto de autenticação fornece id/extras e não os campos arbitrários de usuarios.

## What Changes
Consultar usuarios por auth.id e limitar a saída a id, role e estabelecimento_id antes de aplicar guardas de autorização nos nove endpoints afetados.

## Impact
Exports Xano, testes estáticos e validação real no workspace. Nenhuma ampliação de permissões: o perfil continua vindo do banco, nunca do payload do cliente.

Teste autenticado de finalização também reproduziu acesso inválido a rastreamentos.items: consultas sem paginação retornam arrays. Corrigir iterações em complete, attendant/dashboard, totem/queues e analytics/options; preservar items nas consultas paginadas.

Os testes reais também reproduziram joins inválidos: as referências devem usar os aliases declarados, e campos relacionados exigem eval explícito. Corrigir analytics/report, totem/queues e totem/issue. No painel, carregar serviços por estabelecimento antes de consultar suas filas. Tratar valores opcionais vazios como zero nas consultas SQL do catálogo administrativo e dos filtros de relatório, preservando as guardas de perfil.
