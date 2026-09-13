// Edit aulaflutter record
query "aulaflutter/{aulaflutter_id}" verb=PATCH {
  api_group = "flutter"

  input {
    int aulaflutter_id? filters=min:1
    dblink {
      table = "aulaflutter"
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch aulaflutter {
      field_name = "id"
      field_value = $input.aulaflutter_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $aulaflutter
  }

  response = $aulaflutter
  guid = "OooNUvsEG26_8nqrOm5Dt5UFN_8"
}