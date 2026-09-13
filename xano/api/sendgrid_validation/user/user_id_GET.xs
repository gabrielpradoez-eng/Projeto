// Get user record
query "user/{user_id}" verb=GET {
  api_group = "Sendgrid Validation"

  input {
    int user_id? filters=min:1
  }

  stack {
    db.get "aula sendgrid odair" {
      field_name = "id"
      field_value = $input.user_id
    } as $user
  
    precondition ($user != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $user
  guid = "Y-MHN-WOdVP2smELb1Dv-7xgUPk"
}