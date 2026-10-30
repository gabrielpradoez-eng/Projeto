# Concorrência no Xano — 30/10/2026

## Problema e correção

Duas emissões sobrepostas na fila 4 reproduziram uma falha de unicidade: uma criou o número 4 e outra falhou ao tentar usar o mesmo número. O índice único protegeu o banco, mas a transação não serializava a leitura do último número.

A sintaxe `lock = true` foi confirmada no editor nativo. Os endpoints join, totem/issue, call_next e complete agora bloqueiam a fila dentro da transação e verificam novamente o estado antes da escrita. O cadastro administrativo bloqueia a conta candidata antes de verificar/criar o vínculo. A conclusão também aceita data de término não definida como nulo ou zero, conforme retorno observado no runtime.

As cinco correções foram salvas, validadas pelo parser e publicadas no workspace. O ajuste de data foi publicado em seguida. Ao final, havia zero drafts.

## Execuções reais

Foram usados somente o totem e o atendente de demonstração já existentes, na fila 4 inicialmente vazia. O plano disponível não oferece uma fonte de testes separada; nenhum upgrade foi contratado.

| Cenário | Resultado observado |
|---|---|
| Duas emissões simultâneas após correção | Duas respostas válidas, números 5 e 6 |
| Duas chamadas simultâneas com senhas aguardando | Uma chamou o número 4; outra foi bloqueada por atendimento ativo |
| Duas conclusões simultâneas da mesma senha | Uma concluiu; outra observou que a senha já não estava em atendimento |
| Encerramento dos dados criados | Números 4, 5 e 6 concluídos pelo fluxo normal |
| Dashboard final | Fila 4 vazia e sem atendimento; fila 1 preservada com uma senha aguardando; filas 2 e 3 vazias |

Os registros criados foram as senhas 18, 20 e 21. Foram preservados como histórico concluído; não houve exclusão. Esses ensaios de duas requisições sobrepostas não substituem teste de carga.

## Verificações e limites

224 testes Python aprovados e 23 itens OpenSpec válidos em modo estrito. Quatro regressões de contrato cobrem posicionamento do bloqueio, releitura de estado e proteção do vínculo.

O teste positivo de cadastro de cliente depende de senha definida pelo titular. O teste positivo de vínculo de atendente, inclusive concorrente, depende de confirmação administrativa da conta e do acesso a conceder. Não foram criadas credenciais nem alterados perfis de pessoas para completar os ensaios.
