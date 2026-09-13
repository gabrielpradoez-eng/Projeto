// Update USUARIO record
query "usuario/{usuario_id}" verb=PUT {
  api_group = "CRUD_APIS_BASICO"

  input {
    int usuario_id? filters=min:1
    dblink {
      table = "USUARIO"
    }
  }

  stack {
    db.edit USUARIO {
      field_name = "id"
      field_value = $input.usuario_id
      enforce_hidden_fields = false
      data = {
        nome    : $input.name
        email   : $input.email
        papel_id: $input.papel_id
      }
    } as $model
  }

  response = $model
  guid = "52z9Cm9OF0KQTYVWpq_7WkP-Lpo"
}