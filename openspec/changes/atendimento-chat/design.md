## Decisions
O cliente emite pelo endpoint autenticado. O chat identifica participantes pela senha e pelo vínculo de atendimento, não pela referência pública. O cliente pode reencontrar a conversa ativa mais recente após reconectar; o atendente usa a senha da fila selecionada. A transação bloqueia a fila e relê a situação antes de acessar mensagens, serializando envio e conclusão. A UI atualiza a cada 30 segundos e mostra até 50 mensagens. Dados de mensagens não vão para o log de eventos. A ativação fica desligada até publicar e validar os endpoints.

## Verification
Validar autorização, ciclo da chamada, conteúdo literal, tamanho, transporte e publicação. Nenhuma mensagem de teste será enviada a uma pessoa real.

## Recuperação de consultas

Falhas de leitura pausam o chat por 30/60/120/240 segundos, com estado isolado por usuário e senha na sessão. A contagem é zerada após leitura bem-sucedida. Não são armazenados históricos durante a pausa nem repetidas mutações automaticamente. A confirmação de identidade precede a consulta ou pausa. Isso reduz pressão do chat, sem substituir teste de capacidade da API completa.
