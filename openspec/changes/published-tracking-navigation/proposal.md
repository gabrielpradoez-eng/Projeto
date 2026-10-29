## Why
O teste no aplicativo publicado emitiu a senha 4 corretamente, mas o botão Acompanhar minha senha gerou StreamlitWidgetAlreadyInstantiatedError ao modificar a chave do radio já renderizado. O retorno ao Totem tinha o mesmo padrão.

## What Changes
Executar transições de visão em callbacks de botão antes da reconstrução dos widgets. Validar entrada no rastreamento e retorno em sessões ativas e encerradas.

## Impact
Somente navegação da interface; emissão e estado da senha permanecem no Xano.

O painel publicado também rejeitou o contrato de timestamp numérico do Xano. Normalizar milissegundos UTC no cliente de TV, preservando validação de horários inválidos, e permitir a primeira chamada após snapshot vazio.

Os logs fornecidos em 29/10 registram 94 falhas de atualização automática ao acessar ticket_reference após limpeza da sessão. Cada execução do fragmento deve verificar sessão ativa, referência presente e acompanhamento não encerrado antes de consultar o Xano. Uma execução já agendada após a transição deve terminar sem consulta e sem exceção.
