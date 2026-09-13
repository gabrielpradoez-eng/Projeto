// Delete STATUS_OP record
query "status_op/{status_op_id}" verb=DELETE {
  api_group = "CRUD_APIS_BASICO"

  input {
    int status_op_id? filters=min:1
  }

  stack {
    db.del STATUS_OP {
      field_name = "id"
      field_value = $input.status_op_id
    }
  }

  response = null
  guid = "qp4pBWsMNCIwe99c-IOzN6J6eJI"
}