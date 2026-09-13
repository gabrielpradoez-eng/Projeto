// Add user record
query user verb=POST {
  api_group = "Sendgrid Validation"

  input {
    dblink {
      table = "aula sendgrid odair"
    }
  }

  stack {
    db.add "aula sendgrid odair" {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $user
  }

  response = $user
  guid = "_kXjh6gmej3KM5TuNo3hshl_NeI"
}