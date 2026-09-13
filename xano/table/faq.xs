// Descrição das perguntas e
// respostas mais comuns do site
table FAQ {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    text pergunta? filters=trim
    text resposta? filters=trim
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]

  guid = "kbJBy1lfK83CHr6UWaIoHo4wtxg"
}