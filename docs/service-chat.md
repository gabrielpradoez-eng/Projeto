# Chat privado durante o atendimento

A área Cliente passa a emitir senhas em nome da conta autenticada quando o chat está ativado. O chat abre após a chamada e é encerrado quando o atendente finaliza. O cliente pode reencontrar a conversa ativa mais recente ao entrar novamente. No Núcleo operacional, o atendente vê o chat da senha ativa na fila selecionada, somente se estiver vinculado ao atendimento. O portal atualiza a conversa a cada oito segundos e exibe as últimas 50 mensagens. Não há anexos, notificações externas ou chat via comprovante.

## Ativação

1. Aplicar os três exports indicados no [manifesto](xano-import-order.md). Não criar rotas CRUD para a tabela de mensagens.
2. Com contas de teste em ambiente isolado, emitir como cliente, chamar como atendente e trocar mensagens nos dois sentidos. Verificar rejeição antes da chamada, para outra conta e após a conclusão. Confirmar que o totem e a TV não mostram o conteúdo.
3. Adicionar `service_chat_enabled = true` à seção `[xano]` dos Secrets do Streamlit e confirmar o fluxo publicado. Para desativar a interface, retornar o valor a `false`.

Senhas emitidas anteriormente pela conta técnica do totem não ganham chat, pois não estão vinculadas à identidade do cliente. As mensagens ficam armazenadas no Xano; a interface não oferece acesso após a conclusão. Defina a política de retenção do estabelecimento antes do uso com dados reais.

## Estado da implantação

A tabela foi criada no Xano. A emissão autenticada e o chat foram adicionados ao grupo Queue Management. O rascunho revisado do chat retornou `atendimento: null` e nenhuma mensagem ao consultar sem uma senha chamada. A emissão com o perfil de demonstração foi recusada pela verificação de papel de cliente. Nenhuma senha de teste foi criada. É necessário identificar uma conta de teste com papel de cliente para validar a emissão, a conversa nos dois sentidos e a conclusão antes de publicar a revisão e ativar o portal. O chat segue desativado no portal.
