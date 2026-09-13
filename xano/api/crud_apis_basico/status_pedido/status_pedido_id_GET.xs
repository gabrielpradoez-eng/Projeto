// Get STATUS_PEDIDO record
query "status_pedido/{status_pedido_id}" verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
    int status_pedido_id? filters=min:1
  }

  stack {
    db.get STATUS_PEDIDO {
      field_name = "id"
      field_value = $input.status_pedido_id
    } as $model
  
    precondition ($model != null) {
      error_type = "notfound"
      error = "Not Found"
    }
  }

  response = $model
  guid = "PTamuKxsNDKtBEotwfl5tDuU5w4"
}