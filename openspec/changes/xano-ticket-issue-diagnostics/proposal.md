## Why

Quando o Xano rejeita a emissão de uma senha, a interface mostra somente uma mensagem resumida, dificultando identificar validações específicas do endpoint. O fluxo deve preservar os detalhes seguros da resposta para orientar o diagnóstico sem expor o token do Totem.

## What Changes

- Preservar e apresentar o status HTTP e o corpo de erro retornado pelo Xano nas falhas de emissão, tanto na visão Totem quanto na visão Cliente.
- Registrar diagnóstico estruturado da falha sem registrar credenciais, cabeçalhos de autorização ou dados sensíveis.
- Confirmar por testes que a emissão continua usando `POST /totem/issue`, JSON `{"fila_id": id}` e autenticação server-side já existentes.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `totem-customer-tracking`: detalhar a comunicação de falhas de emissão com status e mensagem/corpo do erro do backend, preservando privacidade das credenciais.

## Impact

- Código: `xano_client.py`, `views/totem_view.py` e `views/client_view.py`.
- Testes: contrato de emissão e apresentação dos detalhes de erro em testes de cliente e Totem.
- API Xano: nenhuma alteração; endpoint, payload e autorização permanecem inalterados.

## Fora de escopo

- Alterar regras de fila, permissões, autenticação ou qualquer endpoint Xano.
- Registrar ou exibir tokens, senhas ou cabeçalhos de autorização.
