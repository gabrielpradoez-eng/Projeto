// Add CEP record
query cep verb=POST {
  api_group = "CRUD_APIS_BASICO"

  input {
    dblink {
      table = "CEP"
    }
  }

  stack {
    db.add CEP {
      enforce_hidden_fields = false
      data = {
        created_at: "now"
        cep       : $input.cep
        uf        : $input.uf
        cidade    : $input.cidade
      }
    } as $model
  }

  response = $model
  guid = "a-jHW94Z3rSAOYnCxG9hT18JC34"
}