// Update aula sendgrid odair record
query "aula_sendgrid_odair/{aula_sendgrid_odair_id}" verb=PUT {
  api_group = "SENDGRID2"

  input {
    int aula_sendgrid_odair_id? filters=min:1
    dblink {
      table = "aula sendgrid odair"
    }
  }

  stack {
    db.edit "aula sendgrid odair" {
      field_name = "id"
      field_value = $input.aula_sendgrid_odair_id
      enforce_hidden_fields = false
      data = {
        email         : $input.email
        otp_code      : $input.otp_code
        otp_express_at: $input.otp_express_at
      }
    } as $model
  }

  response = $model
  guid = "KWh1QEa1hbGr6tGG6FJCjuhmLFU"
}