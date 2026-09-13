// Delete STATUS_PEDIDO record
query "status_pedido/{status_pedido_id}" verb=DELETE {
  api_group = "CRUD_APIS_BASICO"

  input {
    int status_pedido_id? filters=min:1
  }

  stack {
    db.del STATUS_PEDIDO {
      field_name = "id"
      field_value = $input.status_pedido_id
    }
  }

  response = null
  guid = "iCfkz9vsFMFecdkG8RfXe67YF4U"
}