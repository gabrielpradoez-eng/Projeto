query buscaCLIENTE verb=GET {
  api_group = "APIs Customizadas"

  input {
    text authtoken? filters=trim
  }

  stack {
    api.request {
      url = "https://x8ki-letl-twmt.n7.xano.io/api:jjl0Bp3z/auth/me2"
      method = "GET"
      params = $input.authtoken
      headers = [
        "Authorization: Bearer " ~ $input.authtoken
        "Content-Type: application/json"
      ]
    
    } as $api1
  
    conditional {
      if ($api1.response.status == 200) {
        db.get CLIENTE {
          field_name = "usuario_id"
          field_value = `$var.api1.response.result.id`
        } as $CLIENTE1
      }
    
      else {
        var $CLIENTE1 {
          value = {}
        }
      }
    }
  }

  response = $CLIENTE1
  guid = "Ql0BQZLVnm6QTr24h6Up8F9Jw9I"
}