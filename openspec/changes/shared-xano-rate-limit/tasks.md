- [x] Implementar transporte compartilhado sem repetição de mutações.
- [x] Reduzir acompanhamento automático para 30 segundos.
- [x] Executar testes e validação OpenSpec: 253 testes e 28 itens aprovados.
- [x] Publicar nas branches principal e de deploy.
- [x] Validar cliente e atendente em duas sessões simultâneas no aplicativo publicado (25/11/2026), sem HTTP 429 visível neste fluxo.

- [x] Testar login de atendente, atualização e seleção de filas no deploy: sem HTTP 429 visível nessas tentativas. Não comprova capacidade simultânea.
- [x] Corrigir chamada em fila vazia: botão desabilitado quando total_aguardando é zero, evitando HTTP 404 e consumo desnecessário; 253 testes aprovados.
- [x] Validar emissão, chamada com senha, chat nos dois sentidos e finalização após reboot autorizado (25/11/2026). Senha 1 da fila Entrega de aparelho: posição 1, chamada no Guichê 1, mensagens recebidas em ambas as sessões; após finalizar, painel sem atendimento ativo e acompanhamento encerrado. Botão de chamada desabilitado em fila vazia confirmado no deploy.
- [ ] Medir capacidade com muitos usuários e múltiplos processos; a validação de duas sessões não representa teste de carga.

As duas mensagens de validação permanecem no histórico do atendimento encerrado. Nenhuma senha anterior ou conta foi excluída.
