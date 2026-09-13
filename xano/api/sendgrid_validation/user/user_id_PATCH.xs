// Edit user record
query "user/{user_id}" verb=PATCH {
  api_group = "Sendgrid Validation"

  input {
    int user_id? filters=min:1
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
      field_value = $input.user_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $user
  }

  response = $user
  guid = "yC-llBa5B4EVAwhz076XVqZmizY"
}