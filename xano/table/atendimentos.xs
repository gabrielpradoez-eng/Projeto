// Ciclo de vida do atendimento
table atendimentos {
  auth = false

  schema {
    int id
    timestamp created_at?=now
    int senha_id {
      table = "senhas"
    }
  
    int atendente_id {
      table = "atendentes"
    }
  
    timestamp started_at?
    timestamp ended_at?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "senha_id"}]}
    {type: "btree", field: [{name: "atendente_id"}]}
  ]

  guid = "2vCe-cHsizBbfr_e42-p6v839vY"
}