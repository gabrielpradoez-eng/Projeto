// Query all user records
query user verb=GET {
  api_group = "Sendgrid Validation"

  input {
  }

  stack {
    db.query "aula sendgrid odair" {
      return = {type: "list"}
    } as $user
  }

  response = $user
  guid = "s3cd5KSv_mzHxtZpinA1fHp2VvI"
}