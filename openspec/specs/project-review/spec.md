# project-review Specification

## Purpose
Preservar estados confirmados, validar informações operacionais e preparar dados sintéticos de apresentação com segurança.

## Requirements

### Requirement: Estado confirmado preservado
Um cliente com senha confirmada MUST continuar podendo baixar o comprovante e consultar o acompanhamento sem depender do catálogo de filas. Respostas inválidas MUST NOT gerar confirmação de emissão nem quebrar a renderização.

#### Scenario: Catálogo indisponível após emissão
- **WHEN** o catálogo fica indisponível depois da confirmação
- **THEN** o cliente mantém comprovante e acompanhamento; respostas inválidas não geram nova confirmação.

### Requirement: Seleção operacional válida
Se a fila selecionada deixar de existir na resposta autorizada do atendente, a interface MUST selecionar uma opção válida antes de instanciar o widget. IDs inválidos e contagens negativas MUST ser rejeitados.

#### Scenario: Fila selecionada removida
- **WHEN** a seleção anterior não consta nas filas autorizadas
- **THEN** a interface escolhe uma opção válida antes de renderizar o seletor e rejeita contagens negativas.

### Requirement: Histórico de chamadas correto
O feed MUST ordenar por horário de chamada e usar ID apenas como desempate. A TV MUST identificar o serviço quando informado pelo backend para distinguir senhas com o mesmo número em filas diferentes.

#### Scenario: Números repetidos entre serviços
- **WHEN** duas filas possuem senhas com o mesmo número
- **THEN** o feed ordena por horário e ID e a TV identifica os serviços informados.

### Requirement: Dados de demonstração seguros
A preparação MUST usar transação, precondições de escopo e chaves idempotentes. MUST NOT criar credenciais, mudar perfis ou excluir registros. Repetir a execução MUST manter as contagens e não duplicar histórico. O estabelecimento MUST estar identificado como demonstração.

#### Scenario: Repetição da carga de apresentação
- **WHEN** a preparação é repetida no estabelecimento de demonstração
- **THEN** as contagens permanecem iguais sem duplicatas, credenciais novas ou exclusões.

### Requirement: Mensagens adequadas ao perfil
O cliente MUST receber mensagens de erro úteis sem payloads ou códigos internos. Diagnósticos técnicos sanitizados MUST ficar em área recolhida e restrita à interface administrativa.

#### Scenario: Falha exibida ao cliente
- **WHEN** a emissão falha por um erro técnico do backend
- **THEN** o cliente recebe orientação útil e os detalhes sanitizados ficam restritos à área administrativa.
