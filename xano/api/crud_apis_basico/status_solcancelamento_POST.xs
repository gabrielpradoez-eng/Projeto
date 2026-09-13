// Add STATUS_SOLCANCELAMENTO record
query status_solcancelamento verb=POST {
  api_group = "CRUD_APIS_BASICO"

  input {
    dblink {
      table = "STATUS_SOLCANCELAMENTO"
    }
  }

  stack {
    db.add STATUS_SOLCANCELAMENTO {
      enforce_hidden_fields = false
      data = {created_at: "now", status: $input.status}
    } as $model
  }

  response = $model
  guid = "foKr90Umv3uFlF2OoA4sGwsBiYo"
}