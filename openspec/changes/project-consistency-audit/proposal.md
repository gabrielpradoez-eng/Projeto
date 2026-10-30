## Why

A revisão confirmou 190 testes e estrutura OpenSpec válidos, mas o cliente analítico valida apenas os contêineres da resposta. Opções malformadas podem quebrar o cadastro de atendentes e relatórios; seleções antigas e relatórios em cache não são invalidados quando as opções autorizadas mudam. Há checklists desatualizados e a documentação do domínio tem um bloco Markdown sem fechamento.

## What Changes

- Validar opções e campos usados na renderização analítica antes de apresentá-los.
- Redefinir estabelecimento/serviço removidos e limpar relatório quando o catálogo autorizado mudar.
- Cobrir os casos por regressão e executar os testes Python no CI.
- Atualizar evidências, README, contexto arquitetural e situação de GitHub/deploy; preservar pendências reais.
- Sincronizar e arquivar a mudança de navegação por perfil, cuja validação posterior já foi confirmada.

## Capabilities

### Modified Capabilities
- `analytics-and-reports`: respostas válidas e invalidação de opções/relatórios desatualizados.
- `unified-streamlit-experience`: esclarecer login obrigatório e reuso legítimo da sessão administrativa.
- `totem-customer-tracking`: esclarecer que a visão Cliente do portal exige sessão verificada.

## Impact

Cliente analítico, formulário de relatórios, testes e CI. Nenhuma alteração em endpoints, credenciais ou dados Xano. Código publicado na branch existente com PR separado da main.

## Non-goals

Não criar contas, conceder perfis, simular teste de concorrência, alterar credenciais ou fazer merge do PR na main. Registro de versão do site não equivale a cadastro positivo ou teste de carga.
