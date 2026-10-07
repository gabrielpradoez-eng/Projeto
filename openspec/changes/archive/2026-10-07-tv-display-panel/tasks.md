## 1. Feed público e contrato no Xano

- [x] 1.1 Definir cadastro restrito por display, destino público de guichê/sala no atendente e resolução server-side do escopo; verificar nos exports e testes de contrato que display inválido/inativo e tentativa de escopo cruzado são negados e que atendente sem destino não expõe IDs internos.
- [x] 1.2 Implementar endpoint de snapshot público com chamada mais recente, destino, timestamp e até cinco chamadas recentes em ordem definida pelo backend; verificar payload mínimo sem dados de cliente/atendente e estados sem chamada/histórico com os testes de contrato locais.
- [x] 1.3 Integrar o snapshot aos registros canônicos do fluxo `call_next`, mantendo a chamada mais recente após conclusão até ser substituída; verificar os campos snapshot, chave estável e ordenação backend nos exports/testes locais.

## 2. Cliente e painel Streamlit

- [x] 2.1 Criar adaptador REST server-side para o feed Xano, lendo URL/credencial de secrets e sanitizando timeouts/erros; verificar com respostas mockadas e confirmar que nenhum segredo aparece na resposta pública ou nos logs.
- [x] 2.2 Criar entry point Streamlit de display independente, com layout de tela grande e fallback responsivo; verificar que inicia sem login de atendente e que o estado atual ocupa o primeiro plano.
- [x] 2.3 Renderizar chamada atual e até cinco chamadas recentes na ordem do Xano, incluindo estados vazios; verificar que o cliente não reordena nem infere o snapshot.
- [x] 2.4 Implementar polling em fragmento com intervalo inicial de 5 segundos, estado inicial indisponível, sinalização de snapshot desatualizado e recuperação; verificar estados de sucesso, falha inicial, falha após snapshot e recuperação.
- [x] 2.5 Implementar destaque visual e ativação explícita de áudio com deduplicação por identificador de chamada; verificar nova chamada, polls repetidos, chamada inicial já ativa e áudio bloqueado/desativado.

## 3. Testes e publicação

- [x] 3.1 Adicionar testes unitários/AppTest com snapshots mockados para payload privado, escopo, chamada atual, histórico, alertas e recuperação; verificar todos os cenários dos specs relevantes.
- [x] 3.2 Executar suíte completa e validar a change e specs globais; verificar `pytest` sem regressões e comandos OpenSpec sem erros.
- [x] 3.3 Preparar o template de credencial/URL de display e executar o painel local com feed mockado; verificar o entry point Streamlit e registrar publicação no workspace Xano e smoke test em TV como etapa operacional externa, não executada neste ambiente.

Validação deste Apply cobre exports locais, verificações estruturais de contrato e testes mockados. O workspace Xano remoto não está conectado; publicação e smoke test live permanecem pré-requisito operacional antes de expor o display.