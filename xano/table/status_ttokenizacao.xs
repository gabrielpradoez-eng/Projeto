// Status possíveis das Transações de Tokenização
table STATUS_TTOKENIZACAO {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    text status? filters=trim
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]

  guid = "TjtChEFEHz4UAp0qdxVXYjv73YE"
}