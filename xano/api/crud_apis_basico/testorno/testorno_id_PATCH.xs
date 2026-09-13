// Edit TESTORNO record
query "testorno/{testorno_id}" verb=PATCH {
  api_group = "CRUD_APIS_BASICO"

  input {
    int testorno_id? filters=min:1
    dblink {
      table = "TESTORNO"
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch TESTORNO {
      field_name = "id"
      field_value = $input.testorno_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $model
  }

  response = $model
  guid = "a5Gk7H5Ilk9bxm1mLx04IOpz_Wc"
}