// Registro das entradas dos usuários nas filas
table senhas {
  auth = false

  schema {
    int id
    timestamp created_at?=now
    int fila_id {
      table = "filas"
    }
  
    int usuario_id {
      table = "usuarios"
    }
  
    int numero
    enum status?=aguardando {
      values = ["aguardando", "chamado", "concluido", "cancelado"]
    }
  
    timestamp chamado_at?
    timestamp concluido_at?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "fila_id"}, {name: "numero"}]}
    {type: "btree", field: [{name: "fila_id"}]}
    {type: "btree", field: [{name: "usuario_id"}]}
    {type: "btree", field: [{name: "status"}]}
  ]

  guid = "7rhoZnvDbdkmePCpX_mnUvdEeHE"
}