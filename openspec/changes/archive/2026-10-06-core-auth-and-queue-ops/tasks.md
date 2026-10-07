# Tarefas da Change: Núcleo de autenticação, cadastros e fluxo operacional básico da fila

## Objetivo
Implementar a base operacional do FilaSmart em etapas incrementalmente verificáveis, priorizando a consistência do backend e da regra de negócio antes de qualquer interface visual avançada.

## Fase 1 — Base de autenticação e papéis
- [x] Definir e validar modelo de usuários com papéis: admin, atendente, usuario
- [x] Implementar autenticação do usuário no backend do Xano
- [x] Validar token/identidade e recuperação de usuário autenticado
- [x] Definir regras de acesso por papel e por estabelecimento
- [x] Criar mecanismo básico de auditoria de login e ações sensíveis

## Fase 2 — Cadastros de domínio
- [x] Definir e validar tabela de estabelecimentos
- [x] Definir e validar tabela de serviços vinculados a estabelecimento
- [x] Definir e validar tabela de atendentes com vínculo a usuário e estabelecimento
- [x] Validar que cada estabelecimento possui serviços e filas operacionais
- [x] Garantir que o cadastro não permita associar fila a serviço de outro ambiente

## Fase 3 — Gestão de filas
- [x] Definir estrutura de filas com status aberto/fechado
- [x] Validar relacionamento fila → serviço → estabelecimento
- [x] Implementar criação e leitura de filas com regras de integridade
- [x] Garantir que a fila seja a unidade operacional principal do sistema

## Fase 4 — Emissão de senhas
- [x] Implementar geração de senha por fila
- [x] Validar que a fila existe e está aberta
- [x] Calcular número sequencial por fila de forma consistente
- [x] Persistir senha com status aguardando
- [x] Registrar evento de emissão da senha

## Fase 5 — Chamada e atendimento
- [x] Validar que o usuário que chama senha é atendente ativo
- [x] Verificar que a fila pertence ao estabelecimento do atendente
- [x] Buscar a próxima senha em status aguardando
- [x] Alterar o status da senha para chamado
- [x] Criar registro de atendimento com data de início
- [x] Registrar log de chamada da senha

## Fase 6 — Conclusão do atendimento
- [x] Validar que a senha está em estado chamado
- [x] Identificar o atendimento vigente associado à senha
- [x] Encerrar atendimento com data/hora de fim
- [x] Atualizar senha para status concluido
- [x] Registrar evento de encerramento

## Fase 7 — Integridade e observabilidade
- [x] Revisar transações em operações críticas
- [x] Validar preconditions e verificações no backend
- [x] Confirmar persistência de logs para ações de fila, autenticação e atendimento
- [x] Garantir consistência das regras de negócio em diferentes clientes
- [x] Validar que o frontend não reproduz regras de negócio que devem permanecer no backend

## Fase 8 — Validação funcional da entrega
- [x] Testar cenário de usuário comum emitindo senha
- [x] Testar cenário de atendente chamando a próxima senha
- [x] Testar cenário de finalização de atendimento
- [x] Testar cenário de tentativa de acesso indevido por estabelecimento
- [x] Validar fluxo sem filas duplicadas ou números quebrados
- [x] Validar ausência de falhas de integridade no banco e nos logs

## Entrega mínima para a change
A change pode ser considerada pronta quando o fluxo principal abaixo funcionar de ponta a ponta:

1. usuário autentica;
2. atendente e serviço estão vinculados a um estabelecimento;
3. fila está aberta;
4. usuário emite senha;
5. atendente chame a próxima senha;
6. usuário seja atendido e a senha seja concluida;
7. ações críticas sejam registradas em log.

## Critérios de saída
- backend centralizado como fonte de verdade;
- regras de negócio validadas no servidor;
- operações críticas com consistência e auditoria;
- frontend dependente da API e não da lógica de domínio local.
