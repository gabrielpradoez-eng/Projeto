// Sistema para alertas e mensagens aos usuários
table notificacoes {
  auth = false

  schema {
    int id
    timestamp created_at?=now
    int usuario_id {
      table = "usuarios"
    }
  
    text mensagem
    bool lida?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "usuario_id"}]}
  ]

  guid = "N3hDBavgjDpl-Y7sNhHx71N22RM"
}