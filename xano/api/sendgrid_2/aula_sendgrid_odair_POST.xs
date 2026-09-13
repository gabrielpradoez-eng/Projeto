// Add aula sendgrid odair record
query aula_sendgrid_odair verb=POST {
  api_group = "SENDGRID2"

  input {
    dblink {
      table = "aula sendgrid odair"
    }
  }

  stack {
    db.add "aula sendgrid odair" {
      enforce_hidden_fields = false
      data = {
        created_at    : "now"
        email         : $input.email
        otp_code      : $input.otp_code
        otp_express_at: $input.otp_express_at
      }
    } as $model
  }

  response = $model
  guid = "Fs_72s3O2x6iusCpctyrDz-03Xw"
}