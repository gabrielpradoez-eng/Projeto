## MODIFIED Requirements

### Requirement: Public display refreshes from Xano and recovers from errors
O sistema SHALL atualizar periodicamente o snapshot público de chamadas conforme o intervalo selecionado no Painel TV, com padrão de cinco segundos e opções de 3, 5, 10, 15, 30 e 60 segundos. A alteração do intervalo SHALL entrar em vigor sem reiniciar a sessão ou perder o snapshot confirmado, o histórico e o controle de alertas, e o sistema SHALL indicar indisponibilidade ou dados desatualizados sem apresentar um snapshot antigo como atual.

#### Scenario: Polling periódico
- **WHEN** o Painel TV permanece aberto com um intervalo configurado
- **THEN** o sistema SHALL consultar periodicamente o contrato de leitura do Xano segundo esse intervalo e SHALL substituir o snapshot somente por uma resposta válida mais recente.

#### Scenario: Intervalo padrão e opções permitidas
- **WHEN** o Painel TV é aberto sem uma escolha anterior de intervalo
- **THEN** o sistema SHALL iniciar com cinco segundos e SHALL permitir selecionar somente 3, 5, 10, 15, 30 ou 60 segundos.

#### Scenario: Alterar intervalo durante a sessão
- **WHEN** o operador seleciona outro intervalo de atualização
- **THEN** o Painel TV SHALL aplicar a nova frequência sem apagar o último snapshot válido, sem reordenar o histórico e sem emitir novamente o alerta sonoro ou visual para a mesma chamada.

#### Scenario: Falha temporária e recuperação
- **WHEN** uma consulta falha e uma consulta posterior retorna sucesso
- **THEN** o display SHALL indicar que a atualização está indisponível enquanto a falha persistir e SHALL voltar a apresentar o snapshot confirmado quando a conexão se recuperar.
