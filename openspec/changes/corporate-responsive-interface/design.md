## Context
O portal compartilha tema entre perfis, mantendo entradas independentes de totem e TV. Sessões e autorizações permanecem verificadas pelo backend.

## Decisions
Usar azul marinho, branco e cinza com acento azul; trocar ilustração do cabeçalho por contexto de página. Navegação mobile usa widget nativo e sincroniza a seleção com a barra lateral por callback antes da construção dos widgets. Opções derivam exclusivamente de ROLE_VIEWS após verificação de identidade. CSS em containers nomeados apresenta o seletor em até 900px, sem remover a navegação desktop. Formulários preservam rótulos e autocomplete, foco visível e campos de 16px no celular.

## Risks
Seletores data-testid dependem do Streamlit. Manter alterações concentradas, não esconder erros ou controles nativos de abertura do menu. TV em modo apresentação conserva seu fluxo. Testes de estado não substituem inspeção visual nem ensaio em aparelho real.

## Verification
Testes de navegação entre áreas, sincronização e restrição por perfil; suíte existente; validação OpenSpec estrita; inspeção da versão publicada. Registrar separadamente qualquer limite da inspeção em viewport móvel.
