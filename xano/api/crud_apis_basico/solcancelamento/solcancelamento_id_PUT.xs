// Update SOLCANCELAMENTO record
query "solcancelamento/{solcancelamento_id}" verb=PUT {
  api_group = "CRUD_APIS_BASICO"

  input {
    int solcancelamento_id? filters=min:1
    dblink {
      table = "SOLCANCELAMENTO"
    }
  }

  stack {
    db.edit SOLCANCELAMENTO {
      field_name = "id"
      field_value = $input.solcancelamento_id
      enforce_hidden_fields = false
      data = {
        motivo                   : $input.motivo
        pedido_id                : $input.pedido_id
        status_solcancelamento_id: $input.status_solcancelamento_id
      }
    } as $model
  }

  response = $model
  guid = "LyJ9B3GRKX8ha1i3aTBqowC3H4k"
}