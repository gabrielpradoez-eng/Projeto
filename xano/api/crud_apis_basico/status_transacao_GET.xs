// Query all STATUS_TRANSACAO records
query status_transacao verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
  }

  stack {
    db.query STATUS_TRANSACAO {
      return = {type: "list"}
    } as $model
  }

  response = $model
  guid = "YMOhG0niG2C2ycsKY9lY4QSjNhs"
}