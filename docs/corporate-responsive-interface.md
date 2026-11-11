# Interface empresarial e responsiva

## Versão 2026.10.30.2

A interface usa azul marinho, superfícies brancas e cinza claro, cabeçalhos compactos, hierarquia tipográfica e formulários consistentes. A tela inicial apresenta os três perfis e mantém as abas de entrada e cadastro.

Até 900px, um seletor de áreas e o botão de encerrar sessão aparecem no conteúdo. A barra lateral usa o comportamento automático do Streamlit. Até 640px, as colunas e métricas são empilhadas, os botões ocupam a largura disponível e os campos mantêm texto de 16px. Botões têm altura mínima de 46px no desktop e 48px no celular; checkbox oferece área de 44px. O foco de teclado é visível e movimentos são reduzidos conforme preferência do dispositivo.

No portal, os filtros de relatórios ficam em um painel no conteúdo, com campos em duas colunas que empilham em telas pequenas. A entrada independente de relatórios mantém os filtros na barra lateral.

## Verificação

- 229 testes aprovados localmente, incluindo os três perfis na navegação móvel, sincronização com a barra lateral, saída e redução de permissões.
- 24 itens OpenSpec válidos em modo estrito.
- O primeiro CI da main passou. A branch do deploy revelou um teste de expiração que dependia de uptime do servidor maior que 60 segundos. O teste agora usa tempo monotônico relativo, sem alterar a regra de acesso do aplicativo.
- Código publicado na main e na branch codex/streamlit-deployment-preparation.

## Publicação e limites

O aplicativo foi reiniciado no Community Cloud e a versão 2026.10.30.2 foi confirmada em About. As abas Entrar e Criar conta foram inspecionadas no site publicado. Em uma área de 390px no Chromium, o conteúdo empilhou em uma coluna, sem rolagem horizontal, e os campos exibiram texto de 16px. Essa inspeção encontrou sobreposição da barra fixa do Streamlit sobre a marca.

A versão 2026.11.11.1 reserva espaço acima do conteúdo em telas de até 900px para corrigir a sobreposição. A inspeção em largura reduzida no Chromium não substitui um teste em aparelho físico. A navegação por perfil foi verificada pelos testes de estado.

Em 11/11/2026, a aplicação foi reativada e a correção foi observada no ambiente publicado. Com a área do aplicativo reduzida a 390px, a marca começou em 88px, abaixo da barra que termina em 60px. O conteúdo mediu 380px tanto na largura visível quanto na largura rolável, e as colunas ficaram empilhadas. O cadastro exibiu quatro campos com fonte de 16px, botão de 48px e sem rolagem horizontal. O CI de Python aprovou a correção nas duas branches.
