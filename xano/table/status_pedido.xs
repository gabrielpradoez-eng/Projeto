// Status possíveis dos Pedidos
// de Clientes
table STATUS_PEDIDO {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    text status? filters=trim
    text status_para? filters=trim
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {
      type : "btree|unique"
      field: [
        {name: "status", op: "asc"}
        {name: "status_para", op: "asc"}
      ]
    }
  ]

  guid = "4IVmKxfh3gki06Ap6Gj4sg8if40"
}