// Delete ENDERECO record
query "endereco/{endereco_id}" verb=DELETE {
  api_group = "CRUD_APIS_BASICO"

  input {
    int endereco_id? filters=min:1
  }

  stack {
    db.del ENDERECO {
      field_name = "id"
      field_value = $input.endereco_id
    }
  }

  response = null
  guid = "VSzXxAxV8XfAaV9ufEjMM_mOknw"
}