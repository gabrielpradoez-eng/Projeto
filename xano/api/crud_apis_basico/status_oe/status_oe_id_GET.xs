// Get STATUS_OE record
query "status_oe/{status_oe_id}" verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
    int status_oe_id? filters=min:1
  }

  stack {
    db.get STATUS_OE {
      field_name = "id"
      field_value = $input.status_oe_id
    } as $model
  
    precondition ($model != null) {
      error_type = "notfound"
      error = "Not Found"
    }
  }

  response = $model
  guid = "TPl8S_mYFnnvHgw7dHBS5cZJlss"
}