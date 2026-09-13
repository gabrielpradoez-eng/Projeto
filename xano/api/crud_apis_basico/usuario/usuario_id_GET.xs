// Get USUARIO record
query "usuario/{usuario_id}" verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
    int usuario_id? filters=min:1
  }

  stack {
    db.get USUARIO {
      field_name = "id"
      field_value = $input.usuario_id
    } as $model
  
    precondition ($model != null) {
      error_type = "notfound"
      error = "Not Found"
    }
  }

  response = $model
  guid = "enIXMOVeESa3jIizByhk79_bkqE"
}