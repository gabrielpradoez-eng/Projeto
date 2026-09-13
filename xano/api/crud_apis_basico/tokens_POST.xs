// Add TOKENS record
query tokens verb=POST {
  api_group = "CRUD_APIS_BASICO"

  input {
    dblink {
      table = "TOKENS"
    }
  }

  stack {
    db.add TOKENS {
      enforce_hidden_fields = false
      data = {
        created_at: "now"
        plataforma: $input.plataforma
        token     : $input.token
      }
    } as $model
  }

  response = $model
  guid = "UuZMN4G2iW9MFLaC5FNnMBXGT84"
}