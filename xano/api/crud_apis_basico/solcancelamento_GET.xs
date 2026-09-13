// Query all SOLCANCELAMENTO records
query solcancelamento verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
  }

  stack {
    db.query SOLCANCELAMENTO {
      return = {type: "list"}
    } as $model
  }

  response = $model
  guid = "DWRS3LYwBmbPGAjLMCw2w2hGW0s"
}