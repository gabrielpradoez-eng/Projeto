# Proposta de Change: Núcleo de autenticação, cadastros e fluxo operacional básico da fila

## Resumo
Esta change define a primeira entrega incremental do FilaSmart: garantir que o backend e o banco de dados do Xano implementem o núcleo operacional do sistema de filas. O objetivo é estabilizar as regras de negócio que governam autenticação, papéis, cadastro de estabelecimentos e serviços, filas, emissão de senhas, chamada de clientes e encerramento do atendimento.

A entrega será focada em confiabilidade do fluxo principal, segurança de permissões e consistência dos dados, sem avançar ainda para UX refinada, notificações em tempo real, dashboards avançados ou integrações adicionais.

## Problema
O sistema de fila precisa funcionar como fonte de verdade operacional do estabelecimento. Sem um núcleo robusto, todos os painéis, totens e aplicativos ficam dependentes de uma lógica frágil ou inconsistente, o que gera:

- senhas emitidas fora da ordem correta;
- atendentes acessando filas sem permissão;
- status de senhas divergentes dos registros de atendimento;
- métricas e acompanhamento sem base confiável;
- baixa confiança do operador e do cliente no processo.

## Objetivo
Estabelecer a infraestrutura mínima de negócio que permita:

1. autenticar usuários com papéis distintos;
2. registrar estabelecimentos, serviços e filas;
3. emitir senhas em fila aberta;
4. chamar a próxima senha válida para atendimento;
5. registrar o ciclo de atendimento e concluir a senha;
6. manter log de ações críticas para auditoria e troubleshooting.

## Escopo da mudança
Inclui:

- usuários com roles de admin, atendente e usuário;
- autenticação e autorização via backend do Xano;
- vínculo de atendente a estabelecimento;
- cadastro de serviços e filas vinculadas a um estabelecimento;
- abertura/fechamento de fila;
- geração sequencial de números por fila;
- regras de status da senha: aguardando, chamado, concluido e cancelado;
- validação de permissões no backend;
- transações para operações críticas;
- registro de eventos em log para auditoria.

## Fora do escopo (non-goals)
Esta change não inclui:

- UI de totem completa e visual refinada;
- painel público de chamada com anúncios avançados;
- acompanhamento mobile com atualização em tempo real;
- dashboard administrativo com métricas analíticas avançadas;
- notificações push, WebSockets e integrações externas;
- avaliações de satisfação do cliente;
- mecanismos de cancelamento de senha por usuário, além do mínimo obrigatório para operação segura.

## Critérios de sucesso
A mudança será considerada entregue quando:

- o backend validar corretamente permissões por papel e estabelecimento;
- filas e senhas mantiverem ordem e consistência de status;
- o fluxo de chamada e atendimento puder ser executado de ponta a ponta em ambiente de teste;
- registros de auditoria forem criados para ações críticas;
- não houver duplicação de regra de negócio entre frontend e backend.

## Dependências e contexto
Esta mudança é a base do FilaSmart e deve preceder todas as interfaces e integrações do frontend. Ela deve ser implementada com a regra de negócio centralizada no Xano, consumida por Streamlit e Reflex apenas como clientes da API.

## Risco e mitigação
O maior risco desta mudança é a inconsistência operacional da fila. Para mitigar isso, a solução deve priorizar:

- validações no backend;
- operações atômicas em transações;
- registros de auditoria;
- regras simples e verificáveis antes de ampliar o escopo do produto.
