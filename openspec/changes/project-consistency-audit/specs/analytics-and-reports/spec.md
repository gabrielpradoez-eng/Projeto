## ADDED Requirements

### Requirement: Analytics responses are validated before rendering
O cliente MUST rejeitar opções sem identidade e rótulos válidos e relatórios com contagens inválidas, valores não finitos ou coleções malformadas antes de apresentar métricas ou habilitar seleções.

#### Scenario: Opções malformadas
- **WHEN** uma resposta de opções contém estabelecimento sem ID, fila duplicada ou referência a estabelecimento não autorizado
- **THEN** a interface apresenta indisponibilidade sem exceção de renderização nem seleção inválida.

#### Scenario: Relatório inválido
- **WHEN** um relatório contém contagem negativa, número não finito ou filtros e linhas incompatíveis com o contrato
- **THEN** o cliente rejeita o resultado e a interface não apresenta esses dados como métricas válidas.

### Requirement: Analytics selections and cached reports follow current authorized options
A interface MUST redefinir seleções ausentes no catálogo autorizado e descartar relatórios anteriores quando as opções autorizadas mudarem ou não puderem ser confirmadas.

#### Scenario: Estabelecimento ou serviço removido
- **WHEN** a seleção anterior deixa de existir nas opções retornadas
- **THEN** os seletores voltam a valores válidos antes da renderização e o relatório anterior não permanece visível.

#### Scenario: Reordenação sem alteração do escopo
- **WHEN** as mesmas opções são retornadas em outra ordem
- **THEN** o relatório confirmado pode ser preservado sem novas consultas analíticas.
