// Update STATUS_CLIENTE record
query "status_cliente/{status_cliente_id}" verb=PUT {
  api_group = "CRUD_APIS_BASICO"

  input {
    int status_cliente_id? filters=min:1
    dblink {
      table = "STATUS_CLIENTE"
    }
  }

  stack {
    db.edit STATUS_CLIENTE {
      field_name = "id"
      field_value = $input.status_cliente_id
      enforce_hidden_fields = false
      data = {status: $input.status}
    } as $model
  }

  response = $model
  guid = "yryqbBw_3vIqomNsNuxhdtmaDp4"
}