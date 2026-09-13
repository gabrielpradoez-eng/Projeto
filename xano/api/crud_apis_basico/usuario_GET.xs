// Query all USUARIO records
query usuario verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
  }

  stack {
    db.query USUARIO {
      return = {type: "list"}
    } as $model
  }

  response = $model
  guid = "baat4JoRIlmGsziODeidFGBxzu4"
}