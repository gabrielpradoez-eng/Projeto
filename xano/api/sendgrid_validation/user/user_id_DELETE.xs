// Delete user record.
query "user/{user_id}" verb=DELETE {
  api_group = "Sendgrid Validation"

  input {
    int user_id? filters=min:1
  }

  stack {
    db.del "aula sendgrid odair" {
      field_name = "id"
      field_value = $input.user_id
    }
  }

  response = null
  guid = "Y4bIdk_0QzICSRhkefe1sxJ3AyY"
}