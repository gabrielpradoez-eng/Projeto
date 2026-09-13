// Delete aula sendgrid odair record
query "aula_sendgrid_odair/{aula_sendgrid_odair_id}" verb=DELETE {
  api_group = "SENDGRID2"

  input {
    int aula_sendgrid_odair_id? filters=min:1
  }

  stack {
    db.del "aula sendgrid odair" {
      field_name = "id"
      field_value = $input.aula_sendgrid_odair_id
    }
  }

  response = null
  guid = "kuwo4wy2q11DNmLV_-v7Dso3wtU"
}