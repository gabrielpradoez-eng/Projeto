## Implementação
- [x] 1. Simplificar seleções e explicar serviço/fila.
- [x] 2. Tornar relatórios legíveis e preservar contrato UTC e autorização.
- [x] 3. Condicionar reinício e corrigir legenda de atualização.
- [x] 4. Atualizar manual, executar testes e validar OpenSpec.
- [x] 5. Publicar e conferir retorno e versão no deploy.

Validação local em 25/11/2026: 256 testes Python aprovados; 29 itens OpenSpec válidos em modo estrito. Filtros testados com opções únicas/múltiplas, remoção de escopo e envio somente ao solicitar relatório.

Publicação: commit bb1a0b1 nas duas branches. Servidor reiniciado; tela de login disponível e About confirmou versão 2026.11.25.1. As interfaces autenticadas foram verificadas localmente por AppTest; não foi feito novo login administrativo após o reinício. Nenhuma alteração de registros Xano foi necessária.
