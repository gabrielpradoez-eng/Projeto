// Ordens de Produção enviados
// pelo Setor Pedidos ao Setor Cozinha
table OP {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    int status_op_id?=1 {
      table = "STATUS_OP"
    }
  
    int pedido_id? {
      table = "PEDIDO"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]

  guid = "i5bjfLPImcJi7fyHXYyRxeJVv9c"
}