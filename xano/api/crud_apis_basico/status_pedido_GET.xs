// Query all STATUS_PEDIDO records
query status_pedido verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
  }

  stack {
    db.query STATUS_PEDIDO {
      return = {type: "list"}
    } as $model
  }

  response = $model
  guid = "O1RXY8Sp3I3mGwIQGx7eXGcLXdM"
}