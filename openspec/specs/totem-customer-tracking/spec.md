# Totem e Acompanhamento do Cliente Specification

## Purpose

Esta capability permite emitir senhas presenciais em um Totem simples e acompanhar individualmente o andamento da fila. O Xano mantém a autoridade sobre emissão, autorização, status, posição e estimativa, enquanto o Streamlit apresenta os dados ao cliente.

## Requirements

### Requirement: Totem lists queues available for ticket issuance
O sistema SHALL apresentar no Totem somente serviços e filas que o backend autorizar para emissão no estabelecimento selecionado.

#### Scenario: Exibir opções disponíveis
- **WHEN** o Totem solicita as opções de atendimento ao backend
- **THEN** o sistema SHALL mostrar os serviços e filas retornados como disponíveis pelo Xano, sem inferir disponibilidade no cliente.

#### Scenario: Nenhuma fila disponível
- **WHEN** o backend não retorna fila elegível para emissão
- **THEN** o Totem SHALL informar que não há atendimento disponível e SHALL impedir a solicitação de uma senha.

### Requirement: Simplified ticket issuance at the Totem
O sistema SHALL permitir que um cliente emita uma senha selecionando uma fila disponível e confirmando a solicitação, sem expor credenciais de serviço na interface pública.

#### Scenario: Emissão concluída
- **WHEN** o cliente confirma a emissão para uma fila elegível
- **THEN** o backend SHALL validar a fila, criar uma senha na fila e retornar o número e uma referência opaca de acompanhamento, e o Totem SHALL exibir a confirmação.

#### Scenario: Fila deixa de estar disponível
- **WHEN** a fila selecionada é fechada ou deixa de ser elegível antes da confirmação
- **THEN** o backend SHALL rejeitar a emissão sem criar uma senha e o Totem SHALL informar que a fila não está disponível.

#### Scenario: Falha na emissão
- **WHEN** a solicitação de emissão falha por indisponibilidade ou erro de comunicação
- **THEN** o Totem SHALL comunicar que a senha não foi confirmada e SHALL evitar apresentar uma emissão como concluída.

### Requirement: Secure customer ticket tracking
O sistema SHALL permitir acompanhar uma senha usando a referência opaca emitida pelo backend enquanto ela estiver válida e SHALL revelar somente os dados mínimos necessários ao titular dessa referência.

#### Scenario: Consultar senha aguardando
- **WHEN** o cliente consulta uma referência válida cuja senha está aguardando
- **THEN** o backend SHALL retornar status, posição atual na fila e estimativa de espera quando disponível, e a interface SHALL apresentar os valores retornados.

#### Scenario: Senha chamada
- **WHEN** o cliente consulta uma referência válida cuja senha foi chamada
- **THEN** o backend SHALL retornar o status atualizado e SHALL omitir posição de espera quando ela não for aplicável.

#### Scenario: Referência inválida ou não autorizada
- **WHEN** o cliente consulta uma referência inválida, revogada ou não autorizada
- **THEN** o backend SHALL negar os dados da senha e a interface SHALL apresentar uma mensagem genérica sem revelar a existência ou os dados de outras senhas.

#### Scenario: Senha concluída invalida a referência
- **WHEN** a senha associada à referência atinge o status `concluido`
- **THEN** o backend SHALL negar imediatamente novas consultas com essa referência.

#### Scenario: Referência atinge o prazo máximo
- **WHEN** se completam 24 horas desde a emissão da senha
- **THEN** o backend SHALL negar novas consultas com a referência, mesmo que a senha ainda não esteja concluída.

#### Scenario: Encerrar sessão compartilhada do Totem
- **WHEN** uma nova sessão de atendimento é iniciada no Totem compartilhado
- **THEN** a interface SHALL descartar qualquer referência de acompanhamento e resultado anterior antes de aceitar novas interações.

### Requirement: Refresh customer tracking data
O sistema SHALL manter os dados de acompanhamento atualizados por consultas periódicas ao backend e SHALL tratar falhas de atualização sem substituir o último estado confirmado por dados inventados.

#### Scenario: Atualização periódica
- **WHEN** a tela de acompanhamento permanece aberta
- **THEN** a interface SHALL solicitar periodicamente ao Xano o estado mais recente da referência e SHALL apresentar a posição, status e estimativa retornados.

#### Scenario: Falha temporária ao atualizar
- **WHEN** uma consulta periódica falha
- **THEN** a interface SHALL indicar que os dados não puderam ser atualizados e SHALL distinguir o último resultado confirmado de um estado atual desconhecido.

### Requirement: Public client view combines ticket issuance and tracking
O sistema SHALL oferecer na aplicação central uma visão pública de Cliente que permita escolher uma fila retornada pelo backend, solicitar a emissão de senha pelo contrato autorizado do Totem e acompanhar o estado usando a referência opaca retornada, sem expor credenciais do serviço ou dados de outros clientes.

#### Scenario: Cliente consulta filas elegíveis
- **WHEN** o cliente abre a visão pública
- **THEN** a interface SHALL exibir somente as filas disponíveis retornadas pelo backend e SHALL impedir a emissão quando não houver fila elegível.

#### Scenario: Cliente emite senha
- **WHEN** o cliente confirma a emissão para uma fila elegível
- **THEN** o cliente SHALL solicitar a operação ao endpoint autorizado `POST /totem/issue` com o campo `fila_id` e SHALL exibir número e referência de acompanhamento somente após uma resposta válida do backend.

#### Scenario: Cliente acompanha a senha emitida
- **WHEN** existe uma referência válida retornada pelo backend
- **THEN** a visão SHALL consultar o contrato de acompanhamento com essa referência e apresentar o status, posição e estimativa quando disponíveis conforme a resposta do Xano.

#### Scenario: Falha de emissão ou acompanhamento
- **WHEN** o backend rejeita a emissão ou uma consulta de acompanhamento falha
- **THEN** a interface SHALL indicar a falha ou indisponibilidade, SHALL NOT afirmar que uma senha foi emitida sem confirmação e SHALL preservar apenas o último estado de acompanhamento confirmado quando aplicável.

#### Scenario: Nova sessão de cliente
- **WHEN** um novo atendimento é iniciado na visão pública
- **THEN** a interface SHALL descartar a referência, senha e resultado de acompanhamento anteriores antes de aceitar uma nova solicitação.

#### Scenario: Credenciais de serviço permanecem privadas
- **WHEN** a visão pública solicita filas, emissão ou acompanhamento
- **THEN** as credenciais e tokens de serviço SHALL permanecer no lado servidor e SHALL NOT ser exibidos ou enviados ao navegador como conteúdo de interface.