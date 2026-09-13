query cadastraCliente verb=POST {
  api_group = "APIs Customizadas"

  input {
    text nome? filters=trim
    email email? filters=trim|lower
    password senha? {
      sensitive = true
      visibility = "internal"
    }
  
    text celular? filters=trim
    text cpf? filters=trim
    text status? filters=trim
  }

  stack {
    api.request {
      url = "https://x8ki-letl-twmt.n7.xano.io/api:jjl0Bp3z/auth/signup2"
      method = "POST"
      params = {
        nome    : $input.nome
        email   : $input.email
        password: $input.senha
      }
    
      headers = ["Content-Type: application/json"]
    } as $api1
  
    api.request {
      url = "https://x8ki-letl-twmt.n7.xano.io/api:jjl0Bp3z/auth/me2"
      method = "GET"
      params = `{'authtoken: $var.api1.response.result.authToken}`
      headers = [
        "Authorization: Bearer " ~ $var.api1.response.result.authToken
        "Content-Type:application/json"
      ]
    
    } as $api2
  
    db.query STATUS_CLIENTE {
      where = $input.status == $db.STATUS_CLIENTE.status
      return = {type: "list"}
    } as $STATUS_CLIENTE1
  
    db.add CLIENTE {
      enforce_hidden_fields = false
      data = {
        created_at       : `$var.api2.response.result.id`
        celular          : $input.celular
        cpf              : $input.cpf
        status_cliente_id: $var.STATUS_CLIENTE1[0].id
      }
    } as $CLIENTE1
  }

  response = {
    usuario  : $api2.response.result
    cliente  : $CLIENTE1
    authtoken: $api1.response.result.authToken
  }

  guid = "6W4TfwGp7spl2-QEdRiP2YPOSfU"
}