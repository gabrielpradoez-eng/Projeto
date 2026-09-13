// Delete STATUS_TRANSACAO record
query "status_transacao/{status_transacao_id}" verb=DELETE {
  api_group = "CRUD_APIS_BASICO"

  input {
    int status_transacao_id? filters=min:1
  }

  stack {
    db.del STATUS_TRANSACAO {
      field_name = "id"
      field_value = $input.status_transacao_id
    }
  }

  response = null
  guid = "Y1uqeIUGhC6g7ycAEtmKv2MotmQ"
}