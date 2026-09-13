// Get STATUS_TRANSACAO record
query "status_transacao/{status_transacao_id}" verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
    int status_transacao_id? filters=min:1
  }

  stack {
    db.get STATUS_TRANSACAO {
      field_name = "id"
      field_value = $input.status_transacao_id
    } as $model
  
    precondition ($model != null) {
      error_type = "notfound"
      error = "Not Found"
    }
  }

  response = $model
  guid = "-ZWTgP8x_QpT6hq-cisq81PnLMQ"
}