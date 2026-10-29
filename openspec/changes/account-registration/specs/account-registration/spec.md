# Requisitos

- Cliente anônimo pode preencher nome, e-mail, senha e confirmação; senhas divergentes não fazem requisição. Cadastro válido permite entrar pela tela de login.
- Cadastro público nunca aceita perfil privilegiado ou estabelecimento do cliente.
- Só administrador autenticado pode vincular conta de cliente existente a um estabelecimento autorizado e guichê não vazio.
- Conta sem cadastro, perfil privilegiado, vínculo existente ou estabelecimento fora do escopo não produz mutações.
- Vínculo ativo e promoção a atendente são atômicos. Nenhuma senha, hash ou token é retornado no cadastro de atendente.
- Logout e menus existentes mantêm a verificação de sessão.
