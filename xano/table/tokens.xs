// Mantêm as API KEYs de serviços externos, tais como SendGrid e Assas
table TOKENS {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    text plataforma? filters=trim
    text token? filters=trim
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]

  guid = "LeT0ZOir2CS0O1xcQnmHn01pjq4"
}