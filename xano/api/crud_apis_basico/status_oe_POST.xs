// Add STATUS_OE record
query status_oe verb=POST {
  api_group = "CRUD_APIS_BASICO"

  input {
    dblink {
      table = "STATUS_OE"
    }
  }

  stack {
    db.add STATUS_OE {
      enforce_hidden_fields = false
      data = {created_at: "now", status: $input.status}
    } as $model
  }

  response = $model
  guid = "Zl9y7xH48XNG-jFa3mhqNZXLNOg"
}