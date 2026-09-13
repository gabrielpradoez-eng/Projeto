// Delete STATUS_TESTORNO record
query "status_testorno/{status_testorno_id}" verb=DELETE {
  api_group = "CRUD_APIS_BASICO"

  input {
    int status_testorno_id? filters=min:1
  }

  stack {
    db.del STATUS_TESTORNO {
      field_name = "id"
      field_value = $input.status_testorno_id
    }
  }

  response = null
  guid = "RZK5Iu_wwlPp4dW92bG8Dq4XroI"
}