// Get TESTORNO record
query "testorno/{testorno_id}" verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
    int testorno_id? filters=min:1
  }

  stack {
    db.get TESTORNO {
      field_name = "id"
      field_value = $input.testorno_id
    } as $model
  
    precondition ($model != null) {
      error_type = "notfound"
      error = "Not Found"
    }
  }

  response = $model
  guid = "fr2Ksw0HMrD06-c5IlQHOgbjBhQ"
}