//  Status possíveis das Transações de Externo
table STATUS_TESTORNO {
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
    {type: "btree|unique", field: [{name: "status", op: "asc"}]}
  ]

  guid = "RVEjN5q_tVgWPkFWDjYy5YP3yq4"
}