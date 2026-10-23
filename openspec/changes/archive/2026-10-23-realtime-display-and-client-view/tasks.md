## 1. Polling configurável do Painel TV

- [x] 1.1 Adicionar o seletor com padrão de 5 segundos e opções 3, 5, 10, 15, 30 e 60; aplicar o valor dinamicamente ao ciclo de atualização e testar a troca de intervalo sem perda de snapshot ou alerta duplicado.

## 2. Visão pública de Cliente

- [x] 2.1 Criar `views/client_view.py` para listar filas autorizadas e emitir senha pelo cliente Xano existente; testar `POST /totem/issue`, autenticação server-side e payload exato `{"fila_id": id}`.
- [x] 2.2 Integrar o acompanhamento da referência opaca retornada, estado vazio, falhas e início de nova sessão; testar status/posição, retenção apenas do último resultado confirmado e limpeza da referência anterior.

## 3. Navegação e validação integrada

- [x] 3.1 Adicionar a visão Cliente à navegação central sem exigir login administrativo e preservar estados de autenticação e fila; testar navegação, acesso público e separação dos tokens.
- [x] 3.2 Executar regressões de Display, emissão e acompanhamento para confirmar ordem do feed, credenciais privadas, rotas e contratos Xano inalterados.
- [x] 3.3 Executar `.\.venv\Scripts\python.exe -m pytest` e confirmar que toda a suíte passa.
- [x] 3.4 Executar `openspec validate --all` e confirmar que todas as specs e changes são válidas.
