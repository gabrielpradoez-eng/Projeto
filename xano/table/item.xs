// Itens de Pedidos realizados
// pelos Clientes
table ITEM {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    int pedido_id? {
      table = "PEDIDO"
    }
  
    int qtd?=1
    decimal valor_unit?
    decimal subtotal?
    int produto_id? {
      table = "PRODUTO"
    }
  
    int status_item_id? {
      table = "STATUS_ITEM"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {
      type : "btree|unique"
      field: [
        {name: "pedido_id", op: "asc"}
        {name: "produto_id", op: "asc"}
      ]
    }
  ]

  guid = "H-vXIYjDm68GoDd9AtfaOZ8hNPA"
}