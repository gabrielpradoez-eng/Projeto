// Papéis possíveis para os Usuários cadastrados no sistema
table PAPEL {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    text papel? filters=trim
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree|unique", field: [{name: "papel", op: "asc"}]}
  ]

  guid = "PysfrN06b4J5c446W6EkQLRK398"
}