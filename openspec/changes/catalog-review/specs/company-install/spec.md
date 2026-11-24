## ADDED Requirements
### Requirement: Catálogo atualizado após salvar
O portal MUST atualizar os dados confirmados após salvar, sem repetir a escrita, e reconciliar seleções que não estão mais no catálogo.
#### Scenario: Criação confirmada
- **WHEN** um novo serviço e fila são salvos
- **THEN** o portal seleciona a fila confirmada e relê o catálogo sem reenviar a criação.
#### Scenario: Seleção indisponível
- **WHEN** a fila selecionada deixa de constar na resposta autorizada
- **THEN** o formulário volta a uma seleção válida sem renderizar dados antigos.

### Requirement: Configuração resiliente
O portal MUST usar valores padrão seguros quando a seção company não é uma tabela.
#### Scenario: Seção malformada
- **WHEN** company contém um valor escalar ou lista
- **THEN** o portal usa a marca padrão e mantém o catálogo desativado.
