// Transações de Estorno
table TESTORNO {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    decimal valor?
    int status_testorno_id?=1 {
      table = "STATUS_TESTORNO"
    }
  
    int solcancelamento_id? {
      table = "SOLCANCELAMENTO"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]

  guid = "OOXR5W8M5R8VgUbxz_767EG_Aaw"
}