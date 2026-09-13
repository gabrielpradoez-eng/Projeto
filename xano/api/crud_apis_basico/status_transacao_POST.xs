// Add STATUS_TRANSACAO record
query status_transacao verb=POST {
  api_group = "CRUD_APIS_BASICO"

  input {
    dblink {
      table = "STATUS_TRANSACAO"
    }
  }

  stack {
    db.add STATUS_TRANSACAO {
      enforce_hidden_fields = false
      data = {created_at: "now", status: $input.status}
    } as $model
  }

  response = $model
  guid = "ynTSXUgCd_g7kIEbQ5don07ADbw"
}