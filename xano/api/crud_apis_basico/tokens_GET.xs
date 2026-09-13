// Query all TOKENS records
query tokens verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
  }

  stack {
    db.query TOKENS {
      return = {type: "list"}
    } as $model
  }

  response = $model
  guid = "xJcMd48zorjmUcp5mJ2jLCMc6z0"
}