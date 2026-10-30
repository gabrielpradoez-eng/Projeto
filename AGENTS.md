# AGENTS.md — Diretrizes de Atuação para IA

## 1. Contexto e Referências
- Antes de iniciar qualquer alteração ou funcionalidade, consulte os documentos em `docs/project-overview.md` e `docs/domain-model.md`.
- Siga estritamente as regras operacionais e o fluxo de trabalho do OpenSpec.

## 2. Padrões de Código e Arquitetura
- Escreva código limpo, legível, modular e com responsabilidade única.
- Separe claramente as responsabilidades de regra de negócio (backend) das interfaces visuais (frontend e totens/dashboards).
- Reutilize estruturas, utilitários e componentes existentes sempre que possível, evitando duplicação de código.

## 3. Segurança e Regras de Negócio
- Validações de status de senhas, permissões de atendentes e regras de fila devem ser obrigatoriamente processadas no backend.
- Nunca exponha credenciais, senhas ou tokens sensíveis diretamente nos arquivos de código ou em interfaces públicas (como os painéis de chamada).

## 4. Desenvolvimento Incremental
- Qualquer mudança ou implementação deve ser guiada por workflows do OpenSpec.
- Não modifique arquivos ou escopos que não façam parte da change atual sem autorização ou justificativa explícita.

## 5. Estrutura OpenSpec

- Contratos vigentes: `openspec/specs/<capacidade>/spec.md`.
- Trabalho em acompanhamento: `openspec/changes/<mudanca>/`, com proposta, design, tarefas e deltas.
- Histórico: `openspec/changes/archive/<AAAA-MM-DD>-<mudanca>/`, criado após sincronização e verificação.
- Ferramenta fixa: `npm ci --ignore-scripts`; validação: `npm run spec:validate`.
- Instruções e índice: `docs/openspec-workflow.md`.
- Não arquive pendências operacionais como concluídas. Não migre os entrypoints do Streamlit apenas para imitar uma arquitetura que o OpenSpec não exige.
