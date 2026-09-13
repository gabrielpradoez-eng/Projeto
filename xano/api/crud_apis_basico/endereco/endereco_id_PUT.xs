// Update ENDERECO record
query "endereco/{endereco_id}" verb=PUT {
  api_group = "CRUD_APIS_BASICO"

  input {
    int endereco_id? filters=min:1
    dblink {
      table = "ENDERECO"
    }
  }

  stack {
    db.edit ENDERECO {
      field_name = "id"
      field_value = $input.endereco_id
      enforce_hidden_fields = false
      data = {
        cliente_id : $input.cliente_id
        logradouro : $input.logradouro
        numero     : $input.numero
        complemento: $input.complemento
        bairro     : $input.bairro
        referencia : $input.referencia
        padrao     : $input.padrao
        cep_id     : $input.cep_id
      }
    } as $model
  }

  response = $model
  guid = "82xI7MTqMgENXhr8TNnOJM4Djro"
}