// Get the record belonging to the authentication token
query "auth/me2" verb=GET {
  api_group = "Authentication"
  auth = "USUARIO"

  input {
  }

  stack {
    db.get USUARIO {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "created_at", "nome", "email", "papel_id"]
    } as $USUARIO
  }

  response = $USUARIO
  guid = "LGMOm63MHt6tp2G7KN3shZkIBLg"
}