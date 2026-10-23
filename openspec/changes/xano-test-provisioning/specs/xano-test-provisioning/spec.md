## Purpose

Esta capability padroniza o provisionamento repetível de uma instância Xano não produtiva do FilaSmart, com dependências de importação explícitas, dados sintéticos autorizados e credenciais protegidas.

## ADDED Requirements

### Requirement: Xano exports have a dependency-safe import sequence
A documentação SHALL fornecer uma ordem de importação reproduzível para os exports de aplicação em `xano/`, SHALL identificar pré-requisitos de tabelas, grupos e funções e SHALL separar exemplos e exports com referências inválidas do conjunto importável.

#### Scenario: Importar os componentes da aplicação
- **WHEN** uma pessoa provisiona um workspace Xano vazio seguindo a sequência documentada
- **THEN** as tabelas referenciadas SHALL existir antes de funções e endpoints, e cada grupo ou função requerido SHALL existir antes dos endpoints que o utilizam.

#### Scenario: Encontrar um export de exemplo ou referência não resolvida
- **WHEN** o inventário inclui um exemplo de AI, addon de template ou referência de tabela vazia/inválida
- **THEN** a documentação SHALL identificar o arquivo e SHALL instruir a não importá-lo como parte do provisionamento até sua correção explícita.

### Requirement: Test fixtures are scoped to non-production and repeatable
O provisionador SHALL criar o estabelecimento Matriz, um administrador, dois atendentes, serviços e filas de exemplo e uma identidade Totem somente mediante autorização explícita em ambiente não produtivo; execuções repetidas SHALL preservar os registros existentes sem criar duplicatas.

#### Scenario: Criar dados iniciais de teste
- **WHEN** o provisionador autorizado é executado em um workspace de teste vazio
- **THEN** o Xano SHALL receber a Matriz, o administrador `admin@filasmart.com`, os atendentes `atendente1@filasmart.com` e `atendente2@filasmart.com`, e filas Atendimento Geral e Preferencial associadas a serviços e ao mesmo estabelecimento.

#### Scenario: Reexecutar provisionamento
- **WHEN** o provisionador é executado novamente com os mesmos parâmetros
- **THEN** SHALL reutilizar os registros correspondentes por chaves estáveis, não SHALL duplicar usuários, estabelecimento, atendentes, serviços, filas ou credenciais e SHALL relatar o resultado sem expor segredos.

#### Scenario: Tentar provisionar em produção ou sem autorização
- **WHEN** o destino é marcado como produção, ou falta a autorização de seed
- **THEN** o provisionador e o backend SHALL rejeitar a operação antes de modificar qualquer dado.

### Requirement: Test credentials are generated and handled securely
O provisionamento SHALL gerar credenciais próprias para TV e Totem, SHALL gerar senhas iniciais para atendentes, SHALL exibir valores secretos somente uma vez em canal local controlado, SHALL armazenar apenas hashes das credenciais bearer no Xano e SHALL evitar segredos reais ou valores de credencial em logs, respostas de erro e arquivos versionados.

#### Scenario: Criar credencial de display
- **WHEN** o fixture de TV é provisionado
- **THEN** o backend SHALL retornar uma credencial aleatória de uso único, SHALL persistir somente seu hash e SHALL restringir o display ao estabelecimento Matriz.

#### Scenario: Criar identidade Totem
- **WHEN** a identidade de Totem é provisionada
- **THEN** o backend SHALL atribuir o papel Totem e o estabelecimento Matriz e SHALL fornecer uma senha inicial de teste somente uma vez para configuração local.

#### Scenario: Criar contas dos atendentes
- **WHEN** as contas dos dois atendentes são provisionadas
- **THEN** o backend SHALL gerar senhas iniciais distintas e SHALL disponibilizá-las somente uma vez ao operador local autorizado.

#### Scenario: Revisar configuração local
- **WHEN** a pessoa prepara `.streamlit/secrets.toml` usando o modelo versionado
- **THEN** o arquivo SHALL conter apenas placeholders sem credenciais válidas e o arquivo local com valores reais SHALL permanecer fora do controle de versão.

### Requirement: Provisioning contracts are verified without remote side effects
O repositório SHALL testar a sequência e os contratos do provisionador com dependências HTTP simuladas, sem realizar chamadas a um workspace Xano remoto durante a suíte local.

#### Scenario: Validar contratos de criação
- **WHEN** os testes automatizados exercitam o provisionador com respostas simuladas do Xano
- **THEN** SHALL verificar os campos requeridos, relações entre estabelecimento, usuários, serviços e filas, idempotência, validações de destino e ausência de segredos nas saídas.

#### Scenario: Executar a suíte local
- **WHEN** a suíte local é executada sem configuração de credenciais Xano
- **THEN** os testes do provisionador SHALL permanecer determinísticos e SHALL concluir sem acesso de rede.
