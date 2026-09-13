// Get STATUS_ITEM record
query "status_item/{status_item_id}" verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
    int status_item_id? filters=min:1
  }

  stack {
    db.get STATUS_ITEM {
      field_name = "id"
      field_value = $input.status_item_id
    } as $model
  
    precondition ($model != null) {
      error_type = "notfound"
      error = "Not Found"
    }
  }

  response = $model
  guid = "vBkTkk7ahA0CzBvCqwnW_vGpF8k"
}