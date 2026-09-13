// Pedidos realizados pelos clientes
table PEDIDO {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    decimal total?
    text nfc_e? filters=trim
    text? cod_entrega? filters=trim
    int status_pedido_id? {
      table = "STATUS_PEDIDO"
    }
  
    int cliente_id? {
      table = "CLIENTE"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree|unique", field: [{name: "nfc_e", op: "asc"}]}
  ]

  guid = "N69jLoHwer1bAM0YpqDrQtUx-x8"
}