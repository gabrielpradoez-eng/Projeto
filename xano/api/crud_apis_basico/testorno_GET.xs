// Query all TESTORNO records
query testorno verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
  }

  stack {
    db.query TESTORNO {
      return = {type: "list"}
    } as $model
  }

  response = $model
  guid = "NnPHoSvx4gbquofxJz4df3xUrxo"
}