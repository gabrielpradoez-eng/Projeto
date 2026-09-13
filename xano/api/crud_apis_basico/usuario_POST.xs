// Add USUARIO record
query usuario verb=POST {
  api_group = "CRUD_APIS_BASICO"

  input {
    dblink {
      table = "USUARIO"
      override = {nome: {hidden: false}}
    }
  }

  stack {
    db.add USUARIO {
      enforce_hidden_fields = false
      data = {
        created_at: "now"
        nome      : $input.nome
        email     : $input.email
        papel_id  : $input.papel_id
      }
    } as $model
  }

  response = $model
  guid = "R64wxsFD6Uy22MrRbhufcud5eRg"
}