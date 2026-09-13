// Query all aula sendgrid odair records
query aula_sendgrid_odair verb=GET {
  api_group = "SENDGRID2"

  input {
  }

  stack {
    db.query "aula sendgrid odair" {
      return = {type: "list"}
    } as $model
  }

  response = $model
  guid = "bpMSiTX0pCkf35C1eTR6nNbxnVk"
}