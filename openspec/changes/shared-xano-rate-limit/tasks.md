- [x] Implementar transporte compartilhado sem repetição de mutações.
- [x] Reduzir acompanhamento automático para 30 segundos.
- [x] Executar testes e validação OpenSpec: 253 testes e 28 itens aprovados.
- [x] Publicar nas branches principal e de deploy.
- [ ] Validar vários usuários no aplicativo publicado.

- [x] Testar login de atendente, atualização e seleção de filas no deploy: sem HTTP 429 visível nessas tentativas. Não comprova capacidade simultânea.
- [x] Corrigir chamada em fila vazia: botão desabilitado quando total_aguardando é zero, evitando HTTP 404 e consumo desnecessário; 253 testes aprovados.
- [ ] Validar emissão, chamada com senha, chat e finalização entre cliente e atendente após atualização.
