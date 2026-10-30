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

A inspeção do site após a atualização do GitHub ainda apresentou o cabeçalho anterior. Uma sessão nova também mostrou a versão antiga. O botão source confirmou a branch codex/streamlit-deployment-preparation. O gerenciamento do Community Cloud requer login do titular para verificar/reiniciar a publicação. Não foi confirmada a ativação visual da versão 2026.10.30.2.

A ferramenta de navegador disponível não oferece configuração de viewport móvel. Os testes de estado e a revisão dos breakpoints não equivalem a inspeção em um aparelho real. A inspeção visual do layout estreito permanece aberta; não se declara homologação de dispositivos ou conformidade completa com WCAG.
