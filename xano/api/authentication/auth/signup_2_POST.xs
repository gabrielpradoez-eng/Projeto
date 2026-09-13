// Signup and retrieve an authentication token
query "auth/signup2" verb=POST {
  api_group = "Authentication"

  input {
    text nome?
    email email? filters=lower|trim
    password password?
  }

  stack {
    db.get USUARIO {
      field_name = "email"
      field_value = $input.email
    } as $USUARIO
  
    precondition ($USUARIO == null) {
      error_type = "accessdenied"
      error = "This account is already in use."
    }
  
    db.add USUARIO {
      enforce_hidden_fields = false
      data = {
        created_at: "now"
        nome      : $input.nome
        email     : $input.email
        password  : $input.password
      }
    } as $USUARIO
  
    security.create_auth_token {
      table = "USUARIO"
      extras = {}
      expiration = 86400
      id = $USUARIO.id
    } as $authToken
  }

  response = {authToken: $authToken}
  guid = "4P2ZxbXaQjkPxJ_o0WaUUVqt008"
}