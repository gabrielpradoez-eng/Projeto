// Get OE record
query "oe/{oe_id}" verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
    int oe_id? filters=min:1
  }

  stack {
    db.get OE {
      field_name = "id"
      field_value = $input.oe_id
    } as $model
  
    precondition ($model != null) {
      error_type = "notfound"
      error = "Not Found"
    }
  }

  response = $model
  guid = "V84yjZrfm0YbZvQvosQueBZY1cY"
}