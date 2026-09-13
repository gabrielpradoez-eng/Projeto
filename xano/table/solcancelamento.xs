// Solicitações de Cancelamentos
// de Pedidos recebidos do Cliente pelo Setor
table SOLCANCELAMENTO {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    text motivo? filters=trim
    int pedido_id? {
      table = "PEDIDO"
    }
  
    int status_solcancelamento_id? {
      table = "STATUS_SOLCANCELAMENTO"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]

  guid = "_MobjA7ZLxK-SrQRA8hb46WUnVc"
}