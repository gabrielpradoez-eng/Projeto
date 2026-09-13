// Query all STATUS_SOLCANCELAMENTO records
query status_solcancelamento verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
  }

  stack {
    db.query STATUS_SOLCANCELAMENTO {
      return = {type: "list"}
    } as $model
  }

  response = $model
  guid = "XO3F6e7uCc5z5Kr8mTAVbqQUgKo"
}