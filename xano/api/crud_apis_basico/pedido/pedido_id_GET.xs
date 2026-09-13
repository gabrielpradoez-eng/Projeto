// Get PEDIDO record
query "pedido/{pedido_id}" verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
    int pedido_id? filters=min:1
  }

  stack {
    db.get PEDIDO {
      field_name = "id"
      field_value = $input.pedido_id
    } as $model
  
    precondition ($model != null) {
      error_type = "notfound"
      error = "Not Found"
    }
  }

  response = $model
  guid = "t-ykIYiliJVZG1JHef56e7-nivI"
}