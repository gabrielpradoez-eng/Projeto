// Query all TTOKENIZACAO records
query ttokenizacao verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
  }

  stack {
    db.query TTOKENIZACAO {
      return = {type: "list"}
    } as $model
  }

  response = $model
  guid = "pItM_uFZZRK1EwcOpsfS9GvZbRs"
}