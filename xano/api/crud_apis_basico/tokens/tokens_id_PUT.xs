// Update TOKENS record
query "tokens/{tokens_id}" verb=PUT {
  api_group = "CRUD_APIS_BASICO"

  input {
    int tokens_id? filters=min:1
    dblink {
      table = "TOKENS"
    }
  }

  stack {
    db.edit TOKENS {
      field_name = "id"
      field_value = $input.tokens_id
      enforce_hidden_fields = false
      data = {plataforma: $input.plataforma, token: $input.token}
    } as $model
  }

  response = $model
  guid = "0ok0__6PbZ78yVhI2_OAPukEyQA"
}