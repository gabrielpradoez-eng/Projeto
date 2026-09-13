// Add STATUS_TESTORNO record
query status_testorno verb=POST {
  api_group = "CRUD_APIS_BASICO"

  input {
    dblink {
      table = "STATUS_TESTORNO"
    }
  }

  stack {
    db.add STATUS_TESTORNO {
      enforce_hidden_fields = false
      data = {created_at: "now", status: $input.status}
    } as $model
  }

  response = $model
  guid = "jdg96lLVmbJ3lHuQb3OLVK9V7bk"
}