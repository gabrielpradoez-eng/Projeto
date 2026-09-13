// Get aula sendgrid odair record
query "aula_sendgrid_odair/{aula_sendgrid_odair_id}" verb=GET {
  api_group = "SENDGRID2"

  input {
    int aula_sendgrid_odair_id? filters=min:1
  }

  stack {
    db.get "aula sendgrid odair" {
      field_name = "id"
      field_value = $input.aula_sendgrid_odair_id
    } as $model
  
    precondition ($model != null) {
      error_type = "notfound"
      error = "Not Found"
    }
  }

  response = $model
  guid = "N1qLPk6ar70lLQUKe9IFBCVb-8M"
}