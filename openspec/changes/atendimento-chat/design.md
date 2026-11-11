## Decisions
O cliente emite pelo endpoint autenticado. O chat identifica participantes pela senha e pelo vínculo de atendimento, não pela referência pública. O cliente pode reencontrar a conversa ativa mais recente após reconectar; o atendente usa a senha da fila selecionada. A transação bloqueia a fila e relê a situação antes de acessar mensagens, serializando envio e conclusão. A UI atualiza a cada oito segundos e mostra até 50 mensagens. Dados de mensagens não vão para o log de eventos. A ativação fica desligada até publicar e validar os endpoints.

## Verification
Validar autorização, ciclo da chamada, conteúdo literal, tamanho, transporte e publicação. Nenhuma mensagem de teste será enviada a uma pessoa real.
