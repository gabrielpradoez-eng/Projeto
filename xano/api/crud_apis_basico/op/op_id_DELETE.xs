// Delete OP record
query "op/{op_id}" verb=DELETE {
  api_group = "CRUD_APIS_BASICO"

  input {
    int op_id? filters=min:1
  }

  stack {
    db.del OP {
      field_name = "id"
      field_value = $input.op_id
    }
  }

  response = null
  guid = "EGaRTLkemSUJbI0KmQgiJRJqjoY"
}