// Get STATUS_OP record
query "status_op/{status_op_id}" verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
    int status_op_id? filters=min:1
  }

  stack {
    db.get STATUS_OP {
      field_name = "id"
      field_value = $input.status_op_id
    } as $model
  
    precondition ($model != null) {
      error_type = "notfound"
      error = "Not Found"
    }
  }

  response = $model
  guid = "xrRFh6IwnHLiDF1s8MOLKr0TI8s"
}