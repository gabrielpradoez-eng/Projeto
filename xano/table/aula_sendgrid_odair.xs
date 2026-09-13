// aula sendgrid odair
table "aula sendgrid odair" {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    text email? filters=trim
    text otp_code? filters=trim
    timestamp? otp_express_at?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]

  guid = "o2ktIPJxLgDzBr0Tqfn9dq68uKo"
}