## Context

A fila 4 estava vazia; uma emissão paralela criou número 4 e a outra recebeu Duplicate record detected. O schema já contém unicidade fila_id/numero.

## Decisions

Usar locking suportado pelo Xano dentro de db.transaction. Filas são o recurso compartilhado por emissão/chamada/conclusão; a conta candidata é o recurso compartilhado pelo cadastro de vínculo. Ler estados novamente depois de adquirir o bloqueio. Confirmar a sintaxe pelo editor do workspace antes de publicar.

## Verification

Repetir duas solicitações reais em paralelo, verificar números distintos e atendimento único e encerrar os registros criados pelo teste. Não expor tokens ou referências. Testes de contrato complementam a execução no runtime.
