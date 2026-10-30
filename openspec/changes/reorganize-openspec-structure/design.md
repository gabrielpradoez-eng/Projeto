## Context

A base segue `specs/<capability>/spec.md`, `changes/<change>/` e `changes/archive/<date>-<change>/`. Há artefatos abreviados, configurações sem uso pela CLI e histórico de execução distribuído. Consulte proposal.md para motivação.

## Goals / Non-Goals

Padronizar organização e validação sem migrar módulos Python ou alterar o caminho `app.py` configurado no Streamlit. A CLI OpenSpec organiza contratos e mudanças; não prescreve arquitetura de aplicação.

## Decisions

1. Usar OpenSpec 1.15.0 como dependência de desenvolvimento, com lockfile e Node >=20.19. A instalação Python de produção continua independente.
2. Corrigir somente documentação inconsistente com o formato; preservar texto original e tarefas pendentes. Mudanças anteriores recebem metadados de revisão, sem inventar data de criação.
3. Arquivar com sincronização somente `service-experience-refresh` e `project-review-presentation`, cujas tarefas e evidências registram validação no site. Outras entregas históricas aguardam revisão de sincronização; não substituir requisitos vigentes por contratos antigos.
4. A mudança de organização não cria comportamento funcional: usar `skip_specs`, sem requisito fictício para satisfazer o validador.
5. Adicionar índice de situação no guia e README com links relativos. Não renomear os diretórios de domínio existentes.

## Risks / Trade-offs

Histórico pode descrever contratos superados → preservar os documentos históricos e não sincronizá-los automaticamente.
Movimentações podem quebrar links → conferir links Markdown locais e executar testes existentes.
Mudanças operacionais pendentes → manter no diretório ativo e explicitar a situação, sem marcar tarefas como concluídas.

## Migration Plan

Validar baseline, normalizar documentação, sincronizar e arquivar as duas entregas verificadas, executar CLI e testes, criar commits separados de organização e documentação e atualizar a branch do GitHub. Reversão por git revert dos commits, sem migração de dados.
