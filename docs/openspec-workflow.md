# Organização e fluxo OpenSpec

O FilaSmart adota o schema oficial `spec-driven`. A pasta `openspec/` contém contratos, mudanças e histórico; a aplicação Streamlit e os exports Xano continuam separados dessas especificações.

Referências: [site oficial](https://openspec.dev/), [primeiros passos](https://github.com/Fission-AI/OpenSpec/blob/main/docs/getting-started.md), [conceitos](https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md) e [CLI](https://github.com/Fission-AI/OpenSpec/blob/main/docs/cli.md).

## Onde colocar cada informação

| Caminho | Conteúdo |
|---|---|
| `openspec/config.yaml` | Contexto, schema e regras para produzir os artefatos |
| `openspec/specs/<capacidade>/spec.md` | Contrato vigente de comportamento, com requisitos e cenários |
| `openspec/changes/<mudança>/proposal.md` | Problema, escopo, impacto e capacidades afetadas |
| `openspec/changes/<mudança>/design.md` | Decisões técnicas, restrições e riscos |
| `openspec/changes/<mudança>/tasks.md` | Checklist verificável, evidências e pendências |
| `openspec/changes/<mudança>/specs/<capacidade>/spec.md` | Deltas: requisitos adicionados, modificados ou removidos |
| `openspec/changes/<mudança>/.openspec.yaml` | Metadados, schema e exceções documentais previstas pela CLI |
| `openspec/changes/archive/<AAAA-MM-DD>-<mudança>/` | Histórico de uma mudança arquivada |
| `docs/` | Guias para desenvolver, configurar, implantar e operar |

`design.md` pode ser dispensável em mudanças simples segundo o framework; nesta organização foi completado nas mudanças em acompanhamento para registrar decisões e limites. Nas entregas antigas, os arquivos acrescentados retrospectivamente são identificados como formalização documental e não como nova validação operacional.

## Rotina de desenvolvimento

1. Instale a versão fixa com `npm ci --ignore-scripts`.
2. Leia `AGENTS.md`, a visão do projeto, o modelo de domínio e as specs afetadas.
3. Crie uma mudança com `npx --no-install openspec new change nome-da-mudanca`.
4. Consulte `openspec status` e `openspec instructions <artefato>` usando o mesmo nome de mudança. Escreva proposta, deltas, desenho e tarefas antes de implementar.
5. Implemente o escopo aprovado e registre somente tarefas realmente concluídas.
6. Execute `npm run spec:validate` e os testes relevantes. Quando há exports Xano, a validação estática não substitui a execução no runtime.
7. Quando implementação, testes e pendências estiverem resolvidos, use `npx --no-install openspec archive nome-da-mudanca`. A CLI atualiza as specs vigentes e move a mudança para o histórico.

Os comandos `openspec ...` são executados no terminal. Comandos de assistente, como `/opsx:explore`, `/opsx:propose`, `/opsx:apply` e `/opsx:archive`, pertencem ao chat da ferramenta que oferece essa integração.

## Formato de um delta

```markdown
## ADDED Requirements

### Requirement: Acesso verificado
O sistema MUST bloquear funcionalidades protegidas sem identidade confirmada.

#### Scenario: Sessão inválida
- **WHEN** a sessão não é confirmada pelo serviço de identidade
- **THEN** o conteúdo protegido não é apresentado.
```

Use `## MODIFIED Requirements`, `## REMOVED Requirements` e `## RENAMED Requirements` conforme a alteração. Um requisito modificado deve preservar o bloco completo, inclusive os cenários ainda válidos. Capacidades novas incluem `## Purpose` com descrição do domínio.

Mudanças sem alteração de comportamento funcional podem usar `skip_specs: true` em `.openspec.yaml`; não se cria um requisito fictício somente para passar na validação.

## Situação das mudanças

A tabela abaixo é um índice documental. Um checklist concluído não significa que um contrato histórico já pode substituir a spec atual. Entregas antigas potencialmente superadas ficam em acompanhamento até a revisão de sincronização.

| Mudança em acompanhamento | Situação registrada |
|---|---|
| [account-registration](../openspec/changes/account-registration/tasks.md) | 2 tarefa(s) pendente(s); consultar evidências no checklist. |
| [corrigir-login-xano-app](../openspec/changes/corrigir-login-xano-app/tasks.md) | Implementação registrada como concluída; sincronização histórica ainda deve ser revisada. |
| [deployment-access-hardening](../openspec/changes/deployment-access-hardening/tasks.md) | Implementação registrada como concluída; sincronização histórica ainda deve ser revisada. |
| [project-consistency-audit](../openspec/changes/project-consistency-audit/tasks.md) | Revisão atual; evidências em project-audit.md. |
| [published-tracking-navigation](../openspec/changes/published-tracking-navigation/tasks.md) | Implementação registrada como concluída; sincronização histórica ainda deve ser revisada. |
| [queue-debugging](../openspec/changes/queue-debugging/tasks.md) | 1 tarefa(s) pendente(s); consultar evidências no checklist. |
| [reorganize-openspec-structure](../openspec/changes/reorganize-openspec-structure/tasks.md) | Implementação registrada como concluída; sincronização histórica ainda deve ser revisada. |
| [streamlit-deployment-preparation](../openspec/changes/streamlit-deployment-preparation/tasks.md) | 2 tarefa(s) pendente(s); consultar evidências no checklist. |
| [totem-tv-runtime-validation](../openspec/changes/totem-tv-runtime-validation/tasks.md) | Implementação registrada como concluída; sincronização histórica ainda deve ser revisada. |
| [xano-operations-integration](../openspec/changes/xano-operations-integration/tasks.md) | Implementação registrada como concluída; sincronização histórica ainda deve ser revisada. |
| [xano-runtime-identity](../openspec/changes/xano-runtime-identity/tasks.md) | Implementação registrada como concluída; sincronização histórica ainda deve ser revisada. |
| [xano-test-provisioning](../openspec/changes/xano-test-provisioning/tasks.md) | Implementação registrada como concluída; sincronização histórica ainda deve ser revisada. |
| [xano-ticket-issue-diagnostics](../openspec/changes/xano-ticket-issue-diagnostics/tasks.md) | Implementação registrada como concluída; sincronização histórica ainda deve ser revisada. |

## Arquivamentos desta reorganização

Foram arquivadas pela CLI, com sincronização de nove requisitos nas specs vigentes:

- [service-experience-refresh](../openspec/changes/archive/2026-10-30-service-experience-refresh/proposal.md): experiência visual, comprovante e apresentação da TV.
- [project-review-presentation](../openspec/changes/archive/2026-10-30-project-review-presentation/proposal.md): contratos, preservação de estado e dados de demonstração.

Nesta revisão, [verified-role-navigation](../openspec/changes/archive/2026-10-30-verified-role-navigation/proposal.md) também foi sincronizada e arquivada após confirmação de login e logout já registrada. As specs de navegação e Cliente foram alinhadas ao login obrigatório do portal. Os seis diretórios de histórico anteriores à reorganização foram preservados. Cadastro, testes de concorrência e pendências de deploy não foram marcados como concluídos por esta reorganização.

## Validação reproduzível

```bash
npm ci --ignore-scripts
npm run spec:validate
npm run spec:validate:json
python -m pytest -q
```

A CLI valida specs vigentes e mudanças ativas; histórico arquivado não é reescrito automaticamente. O workflow de CI usa a mesma versão e comando da validação local, com acesso somente de leitura ao repositório.
