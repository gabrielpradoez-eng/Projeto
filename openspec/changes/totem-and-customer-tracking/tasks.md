## 1. Contratos e regras no Xano

- [ ] 1.1 Criar identidade de serviço restrita para Totem e endpoint de consulta de serviços/filas elegíveis; verificar que apenas opções abertas e autorizadas são retornadas e que credenciais inválidas são rejeitadas.
- [ ] 1.2 Implementar emissão de senha autorizada para Totem com revalidação da fila, criação consistente sob requisições concorrentes e referência opaca de acompanhamento; verificar emissão, fila fechada e ausência de senhas duplicadas em teste de concorrência.
- [ ] 1.3 Persistir referência de acompanhamento como hash ligado à senha, com expiração/revogação; verificar que a referência bruta não é persistida e que referência expirada ou revogada não autoriza consulta.
- [ ] 1.4 Implementar consulta individual de acompanhamento que retorne somente campos públicos e calcule status, posição e estimativa no Xano; verificar estados aguardando/chamado/concluído, referência inválida e isolamento entre senhas.

## 2. Integração Streamlit

- [ ] 2.1 Criar cliente REST Xano server-side com base URL e credencial em `st.secrets`, timeout limitado e erros sanitizados; verificar contratos e falhas com testes HTTP mockados e confirmar que segredos não aparecem nas respostas ou logs.
- [ ] 2.2 Criar entry point público Streamlit com navegação nativa e páginas em `app_pages/`, preservando o `app.py` operacional existente; verificar que as páginas públicas abrem sem autenticação interativa e que o fluxo operacional anterior não foi alterado.
- [ ] 2.3 Implementar o Totem para listar apenas opções retornadas pelo Xano, confirmar a emissão e exibir número/referência; verificar estados sem filas, fila fechada, sucesso e falha sem confirmação falsa.
- [ ] 2.4 Implementar acompanhamento por referência opaca com exibição dos campos retornados pelo Xano e mensagem genérica para referência inválida; verificar que a interface não expõe dados pessoais, IDs internos ou dados de outra senha.
- [ ] 2.5 Limpar referência e resultado ao iniciar novo atendimento compartilhado e implementar atualização de acompanhamento em fragmento a cada 15 segundos, com atualização manual e estado obsoleto em falha; verificar limpeza entre sessões, atualização e falha temporária.

## 3. Verificação e implantação

- [ ] 3.1 Adicionar testes Streamlit com `AppTest` e respostas Xano simuladas para os cenários de Totem, acompanhamento e isolamento de sessão; verificar que todos os testes novos passam.
- [ ] 3.2 Executar a suíte existente e a nova suíte e validar os artefatos OpenSpec; verificar `pytest` sem regressões e `openspec validate totem-and-customer-tracking` sem erros.
- [ ] 3.3 Configurar secrets e implantar primeiro os endpoints Xano e depois o entry point público; verificar emissão e acompanhamento ponta a ponta em uma fila não produtiva antes de expor o Totem.