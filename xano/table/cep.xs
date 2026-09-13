// CEP dos Clientes cadastrados
table CEP {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    // É um  cep
    text cep? filters=trim
  
    text uf? filters=trim
    text cidade? filters=trim
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree|unique", field: [{name: "cep", op: "asc"}]}
  ]

  guid = "7eRgQwSRXSC272BRTsaG-JglOO0"
}