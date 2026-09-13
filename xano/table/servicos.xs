// Tipos de serviços oferecidos por cada estabelecimento
table servicos {
  auth = false

  schema {
    int id
    timestamp created_at?=now
    int estabelecimento_id {
      table = "estabelecimentos"
    }
  
    text nome
  
    // Tempo estimado de atendimento em minutos
    int tempo_estimado
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "estabelecimento_id"}]}
  ]

  guid = "3pO9d2F51f-PmIlBtDEj-TKg6M8"
}