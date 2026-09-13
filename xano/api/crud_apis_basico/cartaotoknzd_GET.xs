// Query all CARTAOTOKNZD records
query cartaotoknzd verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
  }

  stack {
    db.query CARTAOTOKNZD {
      return = {type: "list"}
    } as $model
  }

  response = $model
  guid = "bcKqS4jsRmKW0Gw2iIhqqGkTQIQ"
}