// Get CARTAOTOKNZD record
query "cartaotoknzd/{cartaotoknzd_id}" verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
    int cartaotoknzd_id? filters=min:1
  }

  stack {
    db.get CARTAOTOKNZD {
      field_name = "id"
      field_value = $input.cartaotoknzd_id
    } as $model
  
    precondition ($model != null) {
      error_type = "notfound"
      error = "Not Found"
    }
  }

  response = $model
  guid = "SSaI_XqWIq9aGUwjUQSnxN8nDOk"
}