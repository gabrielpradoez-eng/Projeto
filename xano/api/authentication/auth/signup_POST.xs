// Signup and retrieve an authentication token
query "auth/signup" verb=POST {
  api_group = "Authentication"

  input {
    text name filters=trim|min:2|max:100
    email email filters=trim|lower
    text password filters=min:10|max:128
  }

  stack {
    // Check if a user record with that email exists
    db.get usuarios {
      field_name = "email"
      field_value = $input.email
    } as $user
  
    // Verify that the email being used to sign up is unique
    precondition ($user == null) {
      error_type = "accessdenied"
      error = "An account with this email already exists."
    }
  
    // Create a new user record
    db.add usuarios {
      data = {
        created_at: "now"
        name      : $input.name
        email     : $input.email
        password  : $input.password
        role      : "usuario"
      }
    } as $user
  
    // Create an authentiction token
    security.create_auth_token {
      table = "usuarios"
      extras = {}
      expiration = 86400
      id = $user.id
    } as $authToken
  
    // Create an event log for signup
    function.run "Quick Start/log_event" {
      input = {user_id: $user.id, action: "signup", metadata: {usuario_id: $user.id}}
    } as $event_log
  }

  response = {authToken: $authToken, user_id: $user.id}
  tags = ["xano:quick-start"]
  guid = "2JsU7Wwk2LLCpdpP7F60w6r10Oc"
}