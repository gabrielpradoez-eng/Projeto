// Query all PRODUTO records
query produto verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
  }

  stack {
    db.query PRODUTO {
      return = {type: "list"}
    } as $model
  }

  response = $model
  guid = "eWKNkNOAsC2l2t28z69mpM1kpGo"
}