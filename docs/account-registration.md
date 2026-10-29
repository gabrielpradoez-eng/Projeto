# Cadastro no FilaSmart

## Cliente

Na tela inicial, abra **Criar conta**, preencha nome, e-mail e senha (10 a 128 caracteres), confirme a senha e envie. Após a confirmação, abra **Entrar** e utilize suas credenciais. O cadastro não escolhe perfil nem libera acesso operacional.

## Atendente

O próprio profissional cria sua conta na tela inicial e define sua senha. Um administrador entra no portal, abre **Administração → Cadastrar atendente**, informa o e-mail exato dessa conta, escolhe o estabelecimento autorizado e o guichê e confirma a liberação. O profissional entra com a mesma senha. Se já estiver conectado, deve sair e entrar novamente para atualizar o perfil.

O Xano exige administrador e verifica o escopo do estabelecimento antes de gravar. Somente contas de cliente sem vínculo de atendimento anterior podem ser cadastradas como atendente. Contas administrativas e técnicas não são convertidas. O vínculo ativo e o perfil são gravados em transação. Falhas não devem ser contornadas alterando dados diretamente na interface.

## Implantação

Atualizar o endpoint público `auth/signup` e publicar `POST admin/attendants` no grupo Queue Management, com autenticação da tabela usuarios. A configuração existente de login_url e base_url é reutilizada. Não há novos secrets. Versão do portal: 2026.10.29.6.

Verificações locais: 190 testes, incluindo validação de campos, senhas divergentes, limpeza de senhas após envio, normalização de e-mail, ausência de perfil no cadastro público e regras de autorização do endpoint de atendentes. O fluxo de criação de uma credencial nova deve ser concluído pelo próprio titular.
