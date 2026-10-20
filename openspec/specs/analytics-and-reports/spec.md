# analytics-and-reports Specification

## Purpose

Esta capability permite que administradores analisem volume e desempenho de filas por período, serviço e fila. O Xano autoriza o escopo e calcula todas as métricas agregadas; o Streamlit apenas apresenta os resultados.

## Requirements

### Requirement: Analytics filter options are authorized by the backend
O sistema SHALL fornecer opções de estabelecimento, serviço e fila somente dentro do escopo permitido ao administrador autenticado.

#### Scenario: Administrador global carrega opções
- **WHEN** um administrador global solicita opções para os filtros do relatório
- **THEN** o backend SHALL retornar os estabelecimentos disponíveis e serviços/filas correspondentes, sem incluir opções fora da autorização daquele administrador.

#### Scenario: Administrador vinculado carrega opções
- **WHEN** um administrador vinculado a um estabelecimento solicita opções para os filtros
- **THEN** o backend SHALL retornar somente serviços e filas daquele estabelecimento e SHALL impedir a seleção de outro estabelecimento.

### Requirement: Authorized analytics scope and period filters
O sistema SHALL permitir consultas analíticas somente a administradores autenticados e SHALL aplicar o escopo do estabelecimento e os filtros de período, serviço e fila no backend.

#### Scenario: Administrador consulta estabelecimento autorizado
- **WHEN** um administrador envia um período válido e um estabelecimento dentro de seu escopo
- **THEN** o backend SHALL retornar agregados limitados ao estabelecimento e aos filtros enviados.

#### Scenario: Administrador vinculado tenta consultar outro estabelecimento
- **WHEN** um administrador associado a um estabelecimento solicita dados de outro estabelecimento
- **THEN** o backend SHALL negar a consulta e SHALL retornar nenhum dado analítico do escopo não autorizado.

#### Scenario: Usuário sem papel administrativo solicita relatório
- **WHEN** um usuário que não é administrador solicita dados analíticos
- **THEN** o backend SHALL negar a consulta independentemente dos filtros enviados.

#### Scenario: Período inválido
- **WHEN** a data inicial é igual ou posterior à data final
- **THEN** o backend SHALL rejeitar a consulta sem retornar agregados.

### Requirement: Analytics summary uses defined event timestamps and samples
O sistema SHALL calcular totais e médias a partir dos timestamps canônicos, usando início inclusivo e fim exclusivo em UTC, e SHALL retornar contagem de amostras para cada média.

#### Scenario: Totais por evento no período
- **WHEN** uma consulta válida contém senhas com timestamps de emissão, chamada e conclusão no período
- **THEN** o backend SHALL contar emissões por `created_at`, chamadas por `chamado_at` e conclusões por `concluido_at`, cada uma somente quando seu próprio timestamp estiver dentro da janela.

#### Scenario: Tempo médio de espera
- **WHEN** existem senhas chamadas no período com `created_at` e `chamado_at` válidos
- **THEN** o backend SHALL calcular a espera como `chamado_at - created_at` e retornar média e quantidade de amostras consideradas.

#### Scenario: Duração média do atendimento
- **WHEN** existem atendimentos encerrados no período com `started_at` e `ended_at` válidos
- **THEN** o backend SHALL calcular a duração como `ended_at - started_at` e retornar média e quantidade de amostras consideradas.

#### Scenario: Sem amostras para uma média
- **WHEN** nenhum registro do período possui os timestamps necessários para uma média
- **THEN** o backend SHALL retornar a média como nula e a contagem de amostras como zero, sem converter ausência de dados em duração zero.

### Requirement: Analytics reports include current status distribution for the issued cohort
O sistema SHALL apresentar a distribuição de status atual dos tickets emitidos no período e SHALL calcular a taxa de conclusão da coorte usando a quantidade emitida no período como denominador.

#### Scenario: Coorte com diferentes status atuais
- **WHEN** o relatório contém tickets emitidos no período que atualmente estão aguardando, chamados, concluídos ou cancelados
- **THEN** o backend SHALL retornar contagens por status atual e calcular a taxa de conclusão como tickets atualmente concluídos divididos pelos tickets emitidos na coorte.

#### Scenario: Coorte sem tickets emitidos
- **WHEN** não há tickets emitidos no período
- **THEN** o backend SHALL retornar contagens iguais a zero e taxa de conclusão nula, sem divisão por zero.

#### Scenario: Status atual não é apresentado como evento histórico
- **WHEN** um ticket emitido no período tem status atual cancelado
- **THEN** o relatório SHALL incluí-lo na distribuição de status atual da coorte e SHALL NOT afirmar que o cancelamento ocorreu dentro do período, pois o modelo não registra timestamp de cancelamento.

### Requirement: Analytics reports provide backend-aggregated trends and breakdowns
O sistema SHALL retornar série temporal e agrupamentos por serviço/fila já agregados e ordenados pelo backend, aplicando a mesma janela, escopo e filtros do resumo.

#### Scenario: Série diária e agrupamento
- **WHEN** o relatório tem dados para mais de um dia ou serviço/fila
- **THEN** o backend SHALL retornar buckets diários em ordem cronológica e agrupamentos identificados por serviço/fila usando os mesmos filtros da consulta.

#### Scenario: Nenhuma linha para o período
- **WHEN** não existem eventos que correspondam aos filtros
- **THEN** o backend SHALL retornar coleções vazias e resumo com contagens zero e médias sem amostra nulas.

### Requirement: Streamlit visualizes analytics without calculating business metrics
O sistema SHALL oferecer filtros e visualizações administrativas e SHALL apresentar os agregados recebidos do Xano sem calcular médias, taxas, totais ou ordenação analítica no cliente.

#### Scenario: Aplicar filtros no relatório
- **WHEN** o administrador seleciona estabelecimento, período, serviço ou fila e solicita atualização
- **THEN** a interface SHALL enviar os filtros ao backend e SHALL renderizar os KPIs, séries e agrupamentos retornados.

#### Scenario: Falha ou ausência de configuração do backend
- **WHEN** a consulta analítica falha ou a integração não está configurada
- **THEN** a interface SHALL indicar indisponibilidade e SHALL NOT apresentar métricas simuladas como dados reais.

### Requirement: Analytics responses protect operational and personal data
O sistema SHALL retornar somente dados agregados necessários à análise e SHALL NOT expor nomes, contatos, credenciais ou identificadores de tickets e usuários.

#### Scenario: Consultar relatório agregado
- **WHEN** um administrador autorizado recebe um relatório
- **THEN** a resposta SHALL conter métricas agregadas e rótulos de serviço/fila sem registros individualizados de clientes ou atendimentos.
