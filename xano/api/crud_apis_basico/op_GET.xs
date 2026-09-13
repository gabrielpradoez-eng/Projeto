// Query all OP records
query op verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
  }

  stack {
    db.query OP {
      return = {type: "list"}
    } as $model
  }

  response = $model
  guid = "7pxggyjoCLW_Q42AYik44jN8WY0"
}