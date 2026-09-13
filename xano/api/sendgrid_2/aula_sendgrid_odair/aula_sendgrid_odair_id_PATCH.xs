// Edit aula sendgrid odair record
query "aula_sendgrid_odair/{aula_sendgrid_odair_id}" verb=PATCH {
  api_group = "SENDGRID2"

  input {
    int aula_sendgrid_odair_id? filters=min:1
    dblink {
      table = "aula sendgrid odair"
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch "aula sendgrid odair" {
      field_name = "id"
      field_value = $input.aula_sendgrid_odair_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $model
  }

  response = $model
  guid = "WK5oH77Qv-0lTFfC436hMqDy8bs"
}