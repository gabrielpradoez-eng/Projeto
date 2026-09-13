// Update CEP record
query "cep/{cep_id}" verb=PUT {
  api_group = "CRUD_APIS_BASICO"

  input {
    int cep_id? filters=min:1
    dblink {
      table = "CEP"
    }
  }

  stack {
    db.edit CEP {
      field_name = "id"
      field_value = $input.cep_id
      enforce_hidden_fields = false
      data = {cep: $input.cep, uf: $input.uf, cidade: $input.cidade}
    } as $model
  }

  response = $model
  guid = "3LqkAjMfLWcLokcJy4gIuAv4GsI"
}