// Delete STATUS_CLIENTE record
query "status_cliente/{status_cliente_id}" verb=DELETE {
  api_group = "CRUD_APIS_BASICO"

  input {
    int status_cliente_id? filters=min:1
  }

  stack {
    db.del STATUS_CLIENTE {
      field_name = "id"
      field_value = $input.status_cliente_id
    }
  }

  response = null
  guid = "52icqvej-TUv5oC1UJnIOgA-Jnw"
}