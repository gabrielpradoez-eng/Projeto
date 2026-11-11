// Mensagens privadas vinculadas ao atendimento, sem CRUD público.
table mensagens_atendimento {
  auth = false
  schema {
    int id
    timestamp created_at?=now
    int atendimento_id {
      table = "atendimentos"
    }
    int remetente_id {
      table = "usuarios"
    }
    text mensagem
  }
  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "atendimento_id"}, {name: "id"}]}
  ]
}
