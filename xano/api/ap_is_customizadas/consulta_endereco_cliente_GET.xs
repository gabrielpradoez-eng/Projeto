query consultaEnderecoCliente verb=GET {
  api_group = "APIs Customizadas"

  input {
    text authtoken? filters=trim
  }

  stack {
    api.request {
      url = "https://x8ki-letl-twmt.n7.xano.io/api:9mPF0785/buscaCLIENTE"
      method = "GET"
      params = {authtoken: $input.authtoken}
      headers = "Authorization: Baerer " ~ $input.authtoken, "Content-Type: application/json"
    } as $api1
  
    db.query ENDERECO {
      return = {type: "list"}
    } as $ENDERECO1
  }

  response = $ENDERECO1
  guid = "92n5ERJIOW-bWJiQz8vQO9wkV5M"
}