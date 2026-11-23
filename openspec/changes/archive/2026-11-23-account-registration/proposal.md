# Cadastro de clientes e atendentes

## Why

Clientes precisam criar a própria conta no portal. Administradores precisam cadastrar o vínculo de atendimento sem depender do editor Xano.

## What Changes

O cadastro público cria exclusivamente o perfil usuario, validando nome, e-mail e senha. O administrador cadastra um atendente a partir do e-mail de uma conta existente, escolhendo estabelecimento e guichê. O backend confirma administrador, escopo e elegibilidade e grava o vínculo e perfil em transação. Contas administrativas/técnicas e vínculos anteriores não são convertidos. A senha é definida pelo próprio titular no cadastro público.

## Non-goals

Fora do escopo: recuperação de senha, envio de convites, verificação de e-mail, remoção de vínculos e troca de estabelecimento.

## Capabilities

### New Capabilities
- `account-registration`: cadastro público e liberação administrativa de atendentes.

### Modified Capabilities
Nenhuma.

## Impact

Formulários Streamlit, autenticação e vínculo persistido no Xano. Estrutura de seções normalizada em 23/11/2026, preservando o escopo da proposta original.
