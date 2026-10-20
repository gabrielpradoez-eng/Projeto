## 1. Contratos e agregações no Xano

- [x] 1.1 Implementar endpoint autenticado de opções analíticas para administradores, respeitando estabelecimento vinculado ou escopo global autorizado; verificar que opções de outros estabelecimentos não são retornadas.
- [x] 1.2 Implementar endpoint de relatório com validação de papel, escopo, período UTC `[início, fim)`, associação serviço/fila e limite máximo de período; verificar rejeição de usuário sem permissão, filtros cruzados, intervalo inválido e intervalo acima do limite.
- [x] 1.3 Calcular no Xano totais por timestamp de evento, espera/duração média com amostras, status atual da coorte e taxa de conclusão definida; verificar fronteiras de período, timestamps ausentes, coorte vazia e ausência de timestamp histórico de cancelamento.
- [x] 1.4 Incluir série diária e agrupamentos por serviço/fila no mesmo envelope, ordenados no backend e sem dados individualizados; verificar filtros idênticos em todas as seções, ordenação e payload sem IDs pessoais ou de ticket.

## 2. Integração e visualização Streamlit

- [x] 2.1 Criar adaptador Xano server-side com URLs em `st.secrets`, timeout limitado e erros sanitizados para opções e relatórios; verificar contratos HTTP mockados e ausência de credenciais em logs/saídas.
- [x] 2.2 Criar visão administrativa Streamlit para carregar opções autorizadas e submeter período, serviço e fila em um formulário; verificar que o cliente não consulta opções fora do backend nem submete filtros antes de selecionar um estabelecimento permitido.
- [x] 2.3 Renderizar KPIs, amostras, status da coorte, série diária e agrupamentos recebidos do Xano; verificar ausência de cálculos/reordenação local e apresentação distinta de média nula versus zero.
- [x] 2.4 Tratar estados de carregamento, sem dados, erro de configuração e falha do serviço sem apresentar dados simulados; verificar cada estado com respostas mockadas.

## 3. Testes e implantação

- [x] 3.1 Adicionar testes unitários/AppTest para autorização, filtros, fronteiras UTC, médias/amostras, status de coorte, ordenação, privacidade e estados da interface; verificar que os novos testes passam.
- [x] 3.2 Executar a suíte completa e validar a change e specs globais; verificar `pytest` sem regressões e validações OpenSpec sem erros.
- [ ] 3.3 Configurar secrets e publicar primeiro os endpoints Xano e depois a visão Streamlit; verificar ponta a ponta em estabelecimento não produtivo antes de habilitar relatórios administrativos.