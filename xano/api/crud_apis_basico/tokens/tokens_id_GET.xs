// Get TOKENS record
query "tokens/{tokens_id}" verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
    int tokens_id? filters=min:1
  }

  stack {
    db.get TOKENS {
      field_name = "id"
      field_value = $input.tokens_id
    } as $model
  
    precondition ($model != null) {
      error_type = "notfound"
      error = "Not Found"
    }
  }

  response = $model
  guid = "YPl95gWJ_T7oKN8OIhno9jVDJcA"
}