// Delete TRANSACAO record
query "transacao/{transacao_id}" verb=DELETE {
  api_group = "CRUD_APIS_BASICO"

  input {
    int transacao_id? filters=min:1
  }

  stack {
    db.del TRANSACAO {
      field_name = "id"
      field_value = $input.transacao_id
    }
  }

  response = null
  guid = "0HbTNoaK-c57Rl_z_v7d8Aybz6M"
}