# TV Display Panel Specification

## Purpose

Esta capability apresenta chamadas de senha atuais e recentes em um display público de sala de espera. O painel orienta clientes por meio de um snapshot mínimo e ordenado pelo Xano, sem controlar filas ou atendimentos.

## Requirements

### Requirement: Public display shows the current call prominently
O sistema SHALL apresentar em destaque a chamada mais recente e seu guichê ou sala, usando exclusivamente o estado retornado pelo backend autorizado para o display, até que outra chamada a substitua.

#### Scenario: Existe chamada atual
- **WHEN** o painel consulta o Xano e recebe uma chamada vigente
- **THEN** o display SHALL mostrar claramente o número da senha e o guichê/sala retornado pelo backend.

#### Scenario: Não há chamada vigente
- **WHEN** o backend informa que não existe chamada atual
- **THEN** o display SHALL apresentar um estado vazio compreensível e SHALL manter disponível o histórico retornado.

#### Scenario: Atendimento da chamada mais recente é concluído
- **WHEN** o atendimento da chamada mais recente é concluído e nenhuma nova chamada foi feita
- **THEN** o display SHALL manter essa chamada em destaque até que outra chamada a substitua.

### Requirement: Public display shows recent calls in backend order
O sistema SHALL apresentar no máximo as cinco chamadas recentes na mesma ordem definida pelo Xano, contendo número da senha e guichê/sala quando fornecido.

#### Scenario: Histórico disponível
- **WHEN** o backend retorna chamadas anteriores à atual
- **THEN** o display SHALL apresentá-las na ordem recebida sem reordenar ou recalcular o histórico no cliente.

#### Scenario: Histórico vazio
- **WHEN** o backend não retorna chamadas recentes
- **THEN** o display SHALL mostrar o histórico vazio sem inventar entradas.

### Requirement: Public display signals a newly observed call
O sistema SHALL sinalizar visualmente uma nova chamada e SHALL tentar emitir um alerta sonoro sem repetir o alerta para o mesmo evento em atualizações consecutivas.

#### Scenario: Nova chamada observada
- **WHEN** o snapshot do backend apresenta um identificador de chamada diferente do último evento confirmado pelo painel
- **THEN** o display SHALL destacar visualmente a nova chamada e SHALL solicitar um alerta sonoro quando a reprodução estiver habilitada pelo navegador.

#### Scenario: Chamada permanece igual
- **WHEN** um novo polling retorna o mesmo identificador de chamada já apresentado
- **THEN** o display SHALL atualizar os dados sem repetir o alerta sonoro ou a animação de nova chamada.

#### Scenario: Áudio bloqueado ou desativado
- **WHEN** o navegador bloqueia a reprodução automática ou o usuário desativa o som
- **THEN** o display SHALL continuar sinalizando visualmente a chamada e SHALL permanecer funcional.

### Requirement: Public display refreshes from Xano and recovers from errors
O sistema SHALL atualizar periodicamente o snapshot público de chamadas e SHALL indicar indisponibilidade ou dados desatualizados sem apresentar um snapshot antigo como atual.

#### Scenario: Polling periódico
- **WHEN** o display permanece aberto
- **THEN** o sistema SHALL consultar periodicamente o contrato de leitura do Xano e SHALL substituir o snapshot somente por uma resposta válida mais recente.

#### Scenario: Falha temporária e recuperação
- **WHEN** uma consulta falha e uma consulta posterior retorna sucesso
- **THEN** o display SHALL indicar que a atualização está indisponível enquanto a falha persistir e SHALL voltar a apresentar o snapshot confirmado quando a conexão se recuperar.

### Requirement: Public display protects private data and scopes its feed
O sistema SHALL retornar apenas dados necessários para orientar clientes e SHALL limitar cada feed público ao estabelecimento ou display autorizado.

#### Scenario: Leitura pública autorizada
- **WHEN** um display autorizado solicita seu snapshot
- **THEN** o backend SHALL retornar chamada atual e histórico mínimo do escopo autorizado sem nome, usuário, contato ou identificador interno de cliente.

#### Scenario: Display sem autorização ou fora do escopo
- **WHEN** uma solicitação usa uma configuração inválida ou tenta consultar outro estabelecimento
- **THEN** o backend SHALL negar a consulta sem retornar dados de chamadas de outro escopo.