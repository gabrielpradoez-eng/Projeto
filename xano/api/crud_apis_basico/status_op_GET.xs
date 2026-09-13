// Query all STATUS_OP records
query status_op verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
  }

  stack {
    db.query STATUS_OP {
      return = {type: "list"}
    } as $model
  }

  response = $model
  guid = "pdCe2whH061TXQcTI-WNpcJ6huk"
}