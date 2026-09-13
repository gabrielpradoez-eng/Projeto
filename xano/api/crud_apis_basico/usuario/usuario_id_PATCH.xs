// Edit USUARIO record
query "usuario/{usuario_id}" verb=PATCH {
  api_group = "CRUD_APIS_BASICO"

  input {
    int usuario_id? filters=min:1
    dblink {
      table = "USUARIO"
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch USUARIO {
      field_name = "id"
      field_value = $input.usuario_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $model
  }

  response = $model
  guid = "XIf_cbkvM9stnRf6g8b0nTnz0_I"
}