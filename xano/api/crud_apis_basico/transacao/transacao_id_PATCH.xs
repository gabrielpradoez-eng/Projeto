// Edit TRANSACAO record
query "transacao/{transacao_id}" verb=PATCH {
  api_group = "CRUD_APIS_BASICO"

  input {
    int transacao_id? filters=min:1
    dblink {
      table = "TRANSACAO"
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch TRANSACAO {
      field_name = "id"
      field_value = $input.transacao_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $model
  }

  response = $model
  guid = "9-4EIXsM_NpEfAFaFPTDK4GrzwM"
}