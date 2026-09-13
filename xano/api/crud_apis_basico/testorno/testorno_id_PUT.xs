// Update TESTORNO record
query "testorno/{testorno_id}" verb=PUT {
  api_group = "CRUD_APIS_BASICO"

  input {
    int testorno_id? filters=min:1
    dblink {
      table = "TESTORNO"
    }
  }

  stack {
    db.edit TESTORNO {
      field_name = "id"
      field_value = $input.testorno_id
      enforce_hidden_fields = false
      data = {
        valor             : $input.valor
        status_testorno_id: $input.status_testorno_id
        solcancelamento_id: $input.solcancelamento_id
      }
    } as $model
  }

  response = $model
  guid = "nrVmDk6du5v1svPKM0IpsJpCkNw"
}