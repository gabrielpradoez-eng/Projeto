// Query all STATUS_TESTORNO records
query status_testorno verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
  }

  stack {
    db.query STATUS_TESTORNO {
      return = {type: "list"}
    } as $model
  }

  response = $model
  guid = "tHqrevcgu4kEEe84Y0yMBVZTRmc"
}