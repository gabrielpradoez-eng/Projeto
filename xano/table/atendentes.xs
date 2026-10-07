// Vínculo entre usuários (staff) e estabelecimentos
table atendentes {
  auth = false

  schema {
    int id
    timestamp created_at?=now
    int usuario_id {
      table = "usuarios"
    }
  
    int estabelecimento_id {
      table = "estabelecimentos"
    }

    text destino_label?
  
    bool ativo?=true
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "usuario_id"}]}
    {type: "btree", field: [{name: "estabelecimento_id"}]}
  ]

  guid = "rmP78u-VOO1BZkyM126x6z7LsVo"
}