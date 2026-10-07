## Why

Clientes na sala de espera precisam identificar rapidamente a senha chamada e o guichê/sala correspondente, enquanto chamadas recentes ajudam a confirmar se perderam uma chamada anterior. O projeto prevê um painel público, mas ainda não há uma interface dedicada nem um contrato específico para consultar e apresentar chamadas sem expor dados operacionais privados.

## What Changes

- Criar um painel público Streamlit pensado para TV/display de sala de espera, com chamada atual em destaque e histórico recente lateral ou inferior.
- Buscar periodicamente no Xano o estado corrente e as últimas chamadas; a ordenação e o estado exibidos permanecem sob autoridade do backend.
- Sinalizar uma nova chamada visualmente e por som, com comportamento acessível e tolerante a navegadores que bloqueiem reprodução automática.
- Apresentar estados vazios, indisponibilidade temporária e recuperação da conexão sem inventar ou conservar como atual um estado não confirmado.
- Restringir a resposta pública aos dados necessários para orientar clientes; não exibir identidade do cliente, dados de autenticação ou metadados internos.
- Fora de escopo: controles de chamada do atendente, gestão de filas, notificações aos clientes, configuração de hardware de áudio/TV e alteração das regras de prioridade ou ordenação.

## Capabilities

### New Capabilities
- `tv-display-panel`: consulta e apresentação pública das chamadas atuais e recentes em display Streamlit.

### Modified Capabilities
- `core-queue-ops`: explicitar que o estado, ordem e destino das chamadas publicados para displays são definidos pelo backend Xano e não podem ser recalculados ou reordenados pelo cliente.

## Impact

- Streamlit: novo entry point/página de display em modo tela cheia e layout responsivo para telas grandes, com polling isolado em fragmento.
- Xano: novo contrato público de leitura por identificador autorizado de display/estabelecimento, retornando a chamada vigente e histórico recente ordenado pelo backend, com payload mínimo.
- Testes: respostas Xano reais ou simuladas para chamada atual, histórico, ausência de chamadas, falhas, reconexão e deduplicação do alerta sonoro/visual.
- Compatibilidade: a tela deve tratar atualização do estado como snapshot autoritativo e não substituir ou reproduzir alerta quando o mesmo evento aparece em polls consecutivos.