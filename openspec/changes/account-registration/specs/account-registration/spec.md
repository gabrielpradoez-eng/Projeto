## Purpose

Definir o cadastro de clientes e a liberação administrativa de atendentes, preservando o controle de perfil e o escopo do estabelecimento.

## ADDED Requirements

### Requirement: Cadastro público de cliente
O sistema MUST aceitar nome, e-mail, senha e confirmação e criar exclusivamente o perfil usuario, sem permitir escolha de privilégios ou estabelecimento.

#### Scenario: Cadastro válido
- **WHEN** uma pessoa fornece nome e e-mail válidos e senhas iguais de 10 a 128 caracteres
- **THEN** a conta de cliente é criada e a pessoa pode entrar pelo formulário de login.

#### Scenario: Senhas divergentes
- **WHEN** a senha e sua confirmação forem diferentes
- **THEN** o formulário informa o problema sem enviar solicitação de criação ao backend.

### Requirement: Liberação administrativa de atendente
O sistema MUST permitir somente ao administrador vincular uma conta cliente existente ao estabelecimento autorizado e a um guichê não vazio.

#### Scenario: Cliente sem vínculo anterior
- **WHEN** o administrador confirma a liberação de uma conta cliente elegível em estabelecimento autorizado
- **THEN** o vínculo ativo e o perfil de atendente são gravados atomicamente sem alterar a senha do titular.

#### Scenario: Perfil ou estabelecimento não elegível
- **WHEN** a conta não existe, possui perfil privilegiado ou vínculo anterior, ou o estabelecimento está fora do escopo
- **THEN** o backend rejeita a operação sem modificar conta ou vínculo.

### Requirement: Credenciais e sessão preservadas
O sistema MUST manter a senha sob controle do titular e não retornar senha, hash ou token no cadastro de atendente; menus e logout MUST continuar sujeitos à verificação de sessão.

#### Scenario: Retorno da liberação
- **WHEN** a liberação de atendente é concluída
- **THEN** a resposta confirma o vínculo sem credenciais e o profissional usa a senha já cadastrada para entrar.
