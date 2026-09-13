// Add OP record
query op verb=POST {
  api_group = "CRUD_APIS_BASICO"

  input {
    dblink {
      table = "OP"
    }
  }

  stack {
    db.add OP {
      enforce_hidden_fields = false
      data = {
        created_at  : "now"
        status_op_id: $input.status_op_id
        pedido_id   : $input.pedido_id
      }
    } as $model
  }

  response = $model
  guid = "DDfxX1aC_3oMJzar_c4StjzVxg4"
}