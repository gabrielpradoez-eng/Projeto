// Query all STATUS_CLIENTE records
query status_cliente verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
  }

  stack {
    db.query STATUS_CLIENTE {
      return = {type: "list"}
    } as $model
  }

  response = $model
  guid = "HlDucDkjCgeSVf8ZPunAAXmyC8g"
}