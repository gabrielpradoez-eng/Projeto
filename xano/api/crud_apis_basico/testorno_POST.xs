// Add TESTORNO record
query testorno verb=POST {
  api_group = "CRUD_APIS_BASICO"

  input {
    dblink {
      table = "TESTORNO"
    }
  }

  stack {
    db.add TESTORNO {
      enforce_hidden_fields = false
      data = {
        created_at        : "now"
        valor             : $input.valor
        status_testorno_id: $input.status_testorno_id
        solcancelamento_id: $input.solcancelamento_id
      }
    } as $model
  }

  response = $model
  guid = "eYEdbdtjQ0f9LsQJ9MSAepjV2aU"
}