// Query all TRANSACAO records
query transacao verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
  }

  stack {
    db.query TRANSACAO {
      return = {type: "list"}
    } as $model
  }

  response = $model
  guid = "Nfh4oe5q4rH-3xChmmT9Zl5h8MI"
}