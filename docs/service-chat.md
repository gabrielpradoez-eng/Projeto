# Chat privado durante o atendimento

A área Cliente passa a emitir senhas em nome da conta autenticada quando o chat está ativado. O chat abre após a chamada e é encerrado quando o atendente finaliza. O cliente pode reencontrar a conversa ativa mais recente ao entrar novamente. No Núcleo operacional, o atendente vê o chat da senha ativa na fila selecionada, somente se estiver vinculado ao atendimento. O portal atualiza a conversa a cada oito segundos e exibe as últimas 50 mensagens. Não há anexos, notificações externas ou chat via comprovante.

## Ativação

1. Aplicar os três exports indicados no [manifesto](xano-import-order.md). Não criar rotas CRUD para a tabela de mensagens.
2. Com contas de teste em ambiente isolado, emitir como cliente, chamar como atendente e trocar mensagens nos dois sentidos. Verificar rejeição antes da chamada, para outra conta e após a conclusão. Confirmar que o totem e a TV não mostram o conteúdo.
3. O portal habilita o chat automaticamente ao usar a API de filas validada do FilaSmart. Para outro ambiente, adicione `service_chat_enabled = true` à seção `[xano]` dos Secrets do Streamlit após validar os endpoints. Defina `false` nessa mesma seção para desativar o chat em qualquer ambiente.

Senhas emitidas anteriormente pela conta técnica do totem não ganham chat, pois não estão vinculadas à identidade do cliente. As mensagens ficam armazenadas no Xano; a interface não oferece acesso após a conclusão. Defina a política de retenção do estabelecimento antes do uso com dados reais.

## Estado da implantação

A tabela e os endpoints de emissão autenticada e de chat estão publicados no Xano. Um teste com dados sintéticos em uma fila de demonstração vazia confirmou a emissão, a descoberta da conversa após a chamada, a leitura e o envio dos dois lados, a recusa de acesso a outro atendente e o bloqueio de leitura e envio após a conclusão. A resposta sempre retorna uma lista de mensagens, inclusive quando a conversa não está disponível.

O Streamlit recebe a ativação junto com o deploy do código. A validação do Xano não substitui o teste autenticado na interface publicada.
