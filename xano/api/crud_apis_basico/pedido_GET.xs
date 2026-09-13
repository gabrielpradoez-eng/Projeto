// Query all PEDIDO records
query pedido verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
  }

  stack {
    db.query PEDIDO {
      return = {type: "list"}
    } as $model
  }

  response = $model
  guid = "tEzkXlz-X2AwMWkNGoWL0gEpC8E"
}