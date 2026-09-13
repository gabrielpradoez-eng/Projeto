query enviar verb=POST {
  api_group = "SENDGRID2"

  input {
    text email? filters=trim
  }

  stack {
    security.random_number {
      min = 100000
      max = 999999
    } as $codigo_otp
  
    var $expiracao {
      value = now|add_secs_to_timestamp:300
    }
  
    db.add "aula sendgrid odair" {
      enforce_hidden_fields = false
      data = {
        email         : $input.email
        otp_code      : $codigo_otp
        otp_express_at: $expiracao
      }
    } as $aula_sendgrid_odair1
  
    function.run sendgrid_basic_send {
      input = {
        to_email: $input.email
        subject : "Sabor Local"
        body    : $codigo_otp
      }
    } as $func1
  }

  response = $codigo_otp
  guid = "JAD0BvnG55AgDN-9JMz_LRJRYuc"
}