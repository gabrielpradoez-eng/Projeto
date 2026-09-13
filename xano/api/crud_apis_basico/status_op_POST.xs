// Add STATUS_OP record
query status_op verb=POST {
  api_group = "CRUD_APIS_BASICO"

  input {
    dblink {
      table = "STATUS_OP"
    }
  }

  stack {
    db.add STATUS_OP {
      enforce_hidden_fields = false
      data = {created_at: "now", status: $input.status}
    } as $model
  }

  response = $model
  guid = "MTT7MwrgMjE11piJRTHEd9t-Vxs"
}