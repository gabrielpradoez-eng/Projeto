## 1. Detalhes de erro do cliente Xano

- [x] 1.1 Preservar o status HTTP, o corpo de resposta limitado e o código/mensagem da API nas exceções de emissão; adicionar testes para JSON estruturado, corpo não JSON e corpo vazio.
- [x] 1.2 Registrar método, caminho e status das falhas sem query strings, payloads ou cabeçalhos sensíveis; testar que o contrato POST e `{"fila_id": id}` permanecem inalterados.

## 2. Feedback nas visões e regressão

- [x] 2.1 Exibir status HTTP e detalhes do Xano nas visões Totem e Cliente, com fallback explícito quando não houver corpo; testar ambas as visões e garantir que tokens não apareçam no erro ou nos logs.
- [x] 2.2 Executar a suíte completa `.\.venv\Scripts\python.exe -m pytest` e confirmar que todos os testes passam.
