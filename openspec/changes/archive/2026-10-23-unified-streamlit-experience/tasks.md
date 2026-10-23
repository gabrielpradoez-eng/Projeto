## 1. Modularização das visões

- [x] 1.1 Extrair a interface administrativa e de relatórios para módulos em `views/`, mantendo autenticação e clientes atuais; verificar com os testes existentes de Admin e Analytics.
- [x] 1.2 Extrair Totem e acompanhamento para módulos em `views/`, preservando emissão, consulta e limpeza ao iniciar nova sessão; verificar com os testes de Totem e acompanhamento.
- [x] 1.3 Extrair o Painel TV para `views/`, preservando escopo, snapshot, polling, ordem e alertas; verificar com os testes do display.

## 2. Navegação e estado centralizados

- [x] 2.1 Tornar `app.py` a entrada central com navegação entre visões e renderização somente da visão selecionada; adicionar teste que valide a seleção/roteamento sem abrir outro aplicativo.
- [x] 2.2 Preservar autenticação, tokens separados, estabelecimento autorizado e filas selecionadas entre navegações; adicionar testes de persistência, isolamento de credenciais e acesso por perfil.
- [x] 2.3 Adaptar `kiosk_app.py`, `tv_display_app.py` e `analytics_app.py` como delegadores temporários quando necessários; verificar que os comandos e testes de entrada existentes continuam funcionais.
- [x] 2.4 Padronizar feedback de carregamento, sucesso, estado vazio, configuração ausente e falha de API nas visões; adicionar testes para respostas vazias e erros sem falsos sucessos.

## 3. Regressão e validação integrada

- [x] 3.1 Atualizar e executar testes de regressão de autenticação, filas do Totem, feed TV, relatórios e navegação; confirmar que rotas, payloads e escopos Xano permanecem compatíveis.
- [x] 3.2 Executar `.\.venv\Scripts\python.exe -m pytest` e `openspec validate --all`; confirmar que a suíte passa e todas as mudanças OpenSpec são válidas.
