// Query all CLIENTE records
query cliente verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
  }

  stack {
    db.query CLIENTE {
      return = {type: "list"}
    } as $model
  }

  response = $model
  guid = "7LsICi4BW52KgMorbYgQU7vVvXU"
}