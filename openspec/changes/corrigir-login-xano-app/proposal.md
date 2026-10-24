## Why

O login administrativo do Streamlit rejeita credenciais válidas do Xano porque o adaptador espera `user_id` no topo da resposta, enquanto o endpoint Live retorna a identidade dentro de `user`. Além disso, a interface usa nomes de papéis diferentes dos valores retornados pelo Xano e contém uma inferência local insegura que pode atribuir papel administrativo a uma identidade remota desconhecida.

## What Changes

- Adaptar o login do backend Streamlit ao contrato Live do Xano (`authToken` e objeto `user`), validando e usando a identidade e o estabelecimento retornados pelo backend.
- Normalizar os papéis `admin`, `atendente` e `usuario` para os valores esperados pela interface; rejeitar respostas ausentes ou malformadas sem inferir identidade ou permissões locais.
- Remover da tela de login a apresentação de usuários de exemplo como se fossem contas utilizáveis.
- Adicionar testes para a resposta real do Xano, normalização dos papéis e rejeição de respostas sem identidade válida.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `core-queue-ops`: o login bem-sucedido deve estabelecer sessão usando a identidade e o papel autoritativos retornados pelo Xano, sem fallback local de privilégio.
- `unified-streamlit-experience`: a interface central deve consumir o contrato Live de autenticação e não sugerir contas de exemplo nem apresentar sessão para respostas inválidas.

## Impact

- Código: `backend_queue.py`, `views/admin_view.py` e possivelmente `app.py`.
- Testes: `tests/test_queue_backend.py` e `tests/test_unified_app.py`.
- Integração: cliente Streamlit e contrato já publicado de `POST /auth/login`; nenhuma mudança de endpoint ou payload Xano é prevista.
- Segurança: identidades, papéis e estabelecimento vêm somente da resposta autenticada do Xano; testes não usarão credenciais reais nem farão chamadas de login ao Live.
