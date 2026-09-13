// Instâncias de filas vinculadas a serviços
table filas {
  auth = false

  schema {
    int id
    timestamp created_at?=now
    int servico_id {
      table = "servicos"
    }
  
    text nome
    enum status?=aberta {
      values = ["aberta", "fechada"]
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "servico_id"}]}
  ]

  guid = "rqdurZtuPHpJSqUexfwOnecnNPk"
}