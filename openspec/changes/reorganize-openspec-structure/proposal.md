## Why

O repositório contém a base OpenSpec, mas 11 de 14 mudanças falham na validação oficial: faltam deltas ou cenários. Não há README na raiz nem comandos reproduzíveis de validação.

## What Changes

- Normalizar os artefatos existentes e completar requisitos com cenários, sem alterar funcionalidades.
- Separar especificações vigentes, mudanças em acompanhamento e histórico arquivado.
- Arquivar as entregas de apresentação e revisão já verificadas, sincronizando seus deltas com as specs vigentes pela CLI oficial.
- Fixar a ferramenta de desenvolvimento, documentar os diretórios e validar o OpenSpec no GitHub Actions.

## Capabilities

Nenhuma capacidade funcional nova ou alterada. Esta é uma reorganização de documentação e ferramentas, com `skip_specs: true`. As correções nos deltas existentes formalizam os requisitos já registrados.

## Impact

`openspec/`, README, guia de contribuição, configuração de desenvolvimento e CI. Os caminhos de entrada do Streamlit, módulos Python, exports Xano e Secrets permanecem compatíveis.

## Non-goals

Não executar deploy, criar contas, concluir pendências operacionais antigas nem alterar regras do atendimento. Mudanças com validação operacional pendente continuam em acompanhamento.
