// Clientes que se cadastraram
// como User e que podem fazer pedidos
table CLIENTE {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    text celular? filters=trim
    text cpf? filters=trim
    int status_cliente_id?=1 {
      table = "STATUS_CLIENTE"
    }
  
    int usuario_id? {
      table = "USUARIO"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree|unique", field: [{name: "cpf", op: "asc"}]}
  ]

  guid = "5R4gMey4u3Mjxv-ZqxO0u6qi0oE"
}