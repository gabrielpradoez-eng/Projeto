// Edit SOLCANCELAMENTO record
query "solcancelamento/{solcancelamento_id}" verb=PATCH {
  api_group = "CRUD_APIS_BASICO"

  input {
    int solcancelamento_id? filters=min:1
    dblink {
      table = "SOLCANCELAMENTO"
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch SOLCANCELAMENTO {
      field_name = "id"
      field_value = $input.solcancelamento_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $model
  }

  response = $model
  guid = "XnN3eMfurd2gX4STtxkcBW7gSAQ"
}