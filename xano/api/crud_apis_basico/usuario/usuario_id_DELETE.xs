// Delete USUARIO record
query "usuario/{usuario_id}" verb=DELETE {
  api_group = "CRUD_APIS_BASICO"

  input {
    int usuario_id? filters=min:1
  }

  stack {
    db.del USUARIO {
      field_name = "id"
      field_value = $input.usuario_id
    }
  }

  response = null
  guid = "uQCk2Udd0Eqix8yzYmeDfRIxlBg"
}