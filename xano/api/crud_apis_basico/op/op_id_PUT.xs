// Update OP record
query "op/{op_id}" verb=PUT {
  api_group = "CRUD_APIS_BASICO"

  input {
    int op_id? filters=min:1
    dblink {
      table = "OP"
    }
  }

  stack {
    db.edit OP {
      field_name = "id"
      field_value = $input.op_id
      enforce_hidden_fields = false
      data = {
        status_op_id: $input.status_op_id
        pedido_id   : $input.pedido_id
      }
    } as $model
  }

  response = $model
  guid = "xqKLbuhT_Pq6_Hjw9aKKkJbCAmM"
}