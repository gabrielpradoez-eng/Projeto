// Login and retrieve an authentication token
query "auth/login2" verb=POST {
  api_group = "Authentication"

  input {
    email email? filters=trim|lower
    text password?
  }

  stack {
    db.get USUARIO {
      field_name = "email"
      field_value = $input.email
      output = ["id", "created_at", "nome", "email", "password"]
    } as $USUARIO
  
    precondition ($USUARIO != null) {
      error = "Invalid Credentials."
    }
  
    security.check_password {
      text_password = $input.password
      hash_password = $USUARIO.password
    } as $pass_result
  
    precondition ($pass_result) {
      error = "Invalid Credentials."
    }
  
    security.create_auth_token {
      table = "USUARIO"
      extras = {}
      expiration = 86400
      id = $USUARIO.id
    } as $authToken
  }

  response = {authToken: $authToken}
  guid = "cPKItB2dtALonm3oCAEJMGiie3k"
}