// Edit PAPEL record
query "papel/{papel_id}" verb=PATCH {
  api_group = "CRUD_APIS_BASICO"

  input {
    int papel_id? filters=min:1
    dblink {
      table = "PAPEL"
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch PAPEL {
      field_name = "id"
      field_value = $input.papel_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $model
  }

  response = $model
  guid = "WQevfUNV2ZmSH9SSTuo91vx7U20"
}