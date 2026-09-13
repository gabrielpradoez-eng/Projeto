// Query all ENDERECO records
query endereco verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
  }

  stack {
    db.query ENDERECO {
      return = {type: "list"}
    } as $model
  }

  response = $model
  guid = "-FC8LzvfGGI2J8-u-QMMt5VLZCg"
}