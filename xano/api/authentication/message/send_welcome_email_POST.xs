// Use this endpoint to send a welcome email to a user
query "message/send_welcome_email" verb=POST {
  api_group = "Authentication"
  auth = "usuarios"

  input {
    // The ID of the user to send the welcome email to.
    int user_id
  }

  stack {
    db.get usuarios {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "role", "estabelecimento_id"]
    } as $actor

    precondition ($actor != null) {
      error_type = "accessdenied"
      error = "Usuário autenticado não encontrado."
    }

    // Retrieve the user record for the given user ID.
    db.get usuarios {
      field_name = "id"
      field_value = $input.user_id
    } as $user_record

    precondition (($actor.role == "admin") || ($auth.id == $input.user_id)) {
      error_type = "accessdenied"
      error = "Você não tem permissão para enviar esta mensagem."
    }
  
    // Ensure the user record exists before proceeding.
    precondition ($user_record != null) {
      error_type = "notfound"
      error = "User not found."
    }
  
    // Set the subject line for the welcome email.
    var $email_subject {
      value = "Welcome to Our Service, " ~ $user_record.name ~ "!"
    }
  
    // Construct the HTML body of the welcome email.
    var $email_body {
      value = "<html><body><h1>Welcome, " ~ $user_record.name ~ "!</h1><p>Thank you for joining our service. We're excited to have you!</p><p>Best regards,<br>The Team</p></body></html>"
    }
  
    // Send welcome email
    util.send_email {
      service_provider = "xano"
      subject = $email_subject
      message = $email_body
    } as $send_email
  
    // Log welcome email sent for user
    function.run "Quick Start/log_event" {
      input = {
        user_id : $input.user_id
        action  : "welcome_email_sent"
        metadata: {}
      }
    } as $event_log
  }

  response = $send_email
  tags = ["xano:quick-start"]
  guid = "SHLN30yeZ96mho8BQOLiZ14lWjg"
}