# Design da Change: Núcleo de autenticação, cadastros e fluxo operacional básico da fila

## Objetivo do design
Descrever a arquitetura e o comportamento do sistema para a primeira entrega incremental, mantendo a regra de negócio centralizada no backend Xano e a interface em Streamlit/Reflex como cliente do sistema.

## Visão arquitetural

### Camadas
1. Frontend cliente
   - Streamlit/Reflex
   - Consome APIs REST do Xano
   - Exibe dados e envia ações do usuário
   - Não deve implementar regras estratégicas de negócio

2. Backend de negócio
   - Xano
   - Persistência de dados
   - Autenticação e autorização
   - Regras de fila, status, permissões e transações

3. Banco de dados
   - Modelo relacional no Xano
   - Registros de usuários, estabelecimentos, serviços, filas, senhas, atendentes e atendimentos

## Entidades centrais

### Usuário
- representa login do sistema;
- possui papel: admin, atendente ou usuario;
- deve ser autenticado no backend antes de qualquer ação sensível.

### Estabelecimento
- representa o local físico ou unidade operativa;
- contém dados básicos do negócio.

### Serviço
- representa o tipo de atendimento disponibilizado;
- pertence a um estabelecimento;
- tem tempo estimado de atendimento em minutos.

### Fila
- instância operacional que agrupa senhas de um serviço;
- possui status aberto/fechado;
- deve estar vinculada a um serviço do estabelecimento.

### Senha
- registro de uma entrada na fila;
- possui número sequencial por fila;
- percorre status: aguardando, chamado, concluido, cancelado.

### Atendente
- vínculo entre usuário e estabelecimento;
- deve possuir status ativo/inativo;
- controla permissões operacionais.

### Atendimento
- representa o ciclo de atendimento de uma senha por um atendente;
- registra início e encerramento.

### Event Log
- registra eventos críticos de negócio para auditoria.

## Regras de negócio principais

### 1. Autenticação e autorização
- Qualquer operação de fila deve exigir autenticação.
- Papéis devem ser validados no backend.
- Atendente só pode operar filas do seu estabelecimento.
- Administrador pode gerenciar configurações e visualizar dados globais.

### 2. Fluxo de fila
- A fila deve ser aberta para receber senhas.
- A emissão de senha exige fila válida e ativa.
- O número da senha deve ser gerado em sequência por fila.
- A próxima senha chamada deve ser a com menor número em status aguardando.

### 3. Atendimento
- Quando a senha é chamada, o sistema muda o status para chamado.
- Deve haver um registro de atendimento vinculado à senha e ao atendente.
- Ao terminar o atendimento, o status da senha passa para concluido.

### 4. Integridade e consistência
- Operações sensíveis devem ser atômicas.
- Precondition e validações de acesso devem ocorrer antes da escrita.
- A fila e o status da senha são fontes de verdade e não devem ser calculados no cliente.

## Fluxos críticos

### Fluxo A: emissão de senha
1. Usuário autenticado solicita fila válida.
2. Sistema verifica se a fila existe e está aberta.
3. Sistema calcula o próximo número disponível.
4. Sistema cria a senha com status aguardando.
5. Sistema registra evento de auditoria.

### Fluxo B: chamada da próxima senha
1. Usuário autenticado verifica se é atendente ativo.
2. Sistema valida que o atendente pertence ao estabelecimento da fila.
3. Sistema localiza a próxima senha aguardando.
4. Sistema atualiza status para chamado e cria o atendimento.
5. Sistema registra evento.

### Fluxo C: conclusão do atendimento
1. Sistema valida que a senha está em atendimento.
2. Sistema localiza o atendimento vigente.
3. Sistema marca a senha como concluida.
4. Sistema encerra o atendimento com data/hora final.
5. Sistema registra evento.

## Padrões de design e arquitetura

### Persistência
- tabelas pequenas e coesas;
- chaves estrangeiras explícitas;
- índices por fila, usuário, status e estabelecimento;
- registros com timestamps para auditoria.

### Segurança
- regras de negócio e permissões no Xano;
- dados sensíveis não expostos em frontends;
- validação de acesso por estabelecimento;
- logs de ações críticas.

### Observabilidade
- event_log para transações de negócio;
- respostas padronizadas para erro de acesso, ausência de fila ou regra violada;
- uso de dados de auditoria para diagnóstico e validação de qualidade.

## Dependências entre módulos
A primeira entrega requer o alinhamento dos seguintes módulos:

- autenticação/usuários;
- cadastro de estabelecimento;
- serviços e filas;
- status de senha;
- atendimento;
- logging.

Sem esse conjunto integrado, nenhum frontend de totem, painel ou dashboard consegue operar com consistência.

## Critérios de qualidade do design
- centralização da regra de negócio no backend;
- baixa dependência de UI para decisão de fluxo;
- pouca duplicação de lógica;
- transações em operações críticas;
- clareza de status e eventos.

## Riscos de design e mitigação

### Risco: concorrência em fila
Mitigação: transações e busca por próximo número em contexto de fila.

### Risco: fuga de permissão
Mitigação: validação rígida com estabelecimento e papel no backend.

### Risco: inconsistência entre frontend e backend
Mitigação: frontend somente consumindo estado do backend e nunca decidindo regra de fila.

### Risco: ausência de observabilidade
Mitigação: logs de ações críticas e status rastreáveis.
