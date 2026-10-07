## 1. Contratos e regras no Xano

- [x] 1.1 Adicionar perfil Xano `totem` vinculado a um estabelecimento e endpoint de consulta de serviços/filas elegíveis; validar o contrato de escopo e rejeição de acesso usando os testes de contrato/mock aprovados.
- [x] 1.2 Implementar emissão de senha autorizada para Totem com revalidação da fila, restrição única por fila/número e referência opaca de acompanhamento; validar payloads de emissão e rejeição com os testes de contrato/mock aprovados.
- [x] 1.3 Persistir referência de acompanhamento como hash ligado à senha e expirar o acesso ao concluir ou após 24 horas desde a emissão, o que ocorrer primeiro; validar o contrato de expiração e revogação com os testes de contrato/mock aprovados.
- [x] 1.4 Implementar consulta individual de acompanhamento que retorne somente campos públicos e calcule status, posição e estimativa no Xano; validar a resposta mínima e os casos de referência inválida/encerrada com os testes de contrato/mock aprovados.

## 2. Integração Streamlit

- [x] 2.1 Criar cliente REST Xano server-side com base URL e credencial em `st.secrets`, timeout limitado e erros sanitizados; verificar contratos e falhas com testes HTTP mockados e confirmar que segredos não aparecem nas respostas ou logs.
- [x] 2.2 Criar entry point público Streamlit com navegação nativa e páginas em `app_pages/`, preservando o `app.py` operacional existente; verificar que as páginas públicas abrem sem autenticação interativa e que o fluxo operacional anterior não foi alterado.
- [x] 2.3 Implementar o Totem para listar apenas opções retornadas pelo Xano, confirmar a emissão e exibir número/referência; verificar estados sem filas, fila fechada, sucesso e falha sem confirmação falsa.
- [x] 2.4 Implementar acompanhamento por referência opaca com exibição dos campos retornados pelo Xano e mensagem genérica para referência inválida/encerrada; verificar que a interface não expõe dados pessoais, IDs internos ou dados de outra senha.
- [x] 2.5 Limpar referência e resultado ao iniciar novo atendimento compartilhado e implementar atualização de acompanhamento em fragmento a cada 15 segundos, com atualização manual e estado obsoleto em falha; verificar limpeza entre sessões, atualização e falha temporária.

## 3. Verificação e implantação

- [x] 3.1 Adicionar testes Streamlit com `AppTest` e respostas Xano simuladas para os cenários de Totem, acompanhamento e isolamento de sessão; verificar que todos os testes novos passam.
- [x] 3.2 Executar a suíte existente e a nova suíte e validar os artefatos OpenSpec; verificar `pytest` sem regressões e `openspec validate totem-and-customer-tracking` sem erros.
- [x] 3.3 Preparar os secrets e pré-requisitos para publicar primeiro os endpoints Xano e depois o entry point público; verificar o template de configuração e manter o smoke test live como passo operacional após provisionar o workspace Xano.