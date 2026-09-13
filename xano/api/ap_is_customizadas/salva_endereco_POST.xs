query salvaEndereco verb=POST {
  api_group = "APIs Customizadas"

  input {
    text logradouro? filters=trim
    text numero? filters=trim
    text complemento? filters=trim
    text referencia? filters=trim
    text cep? filters=trim
    text cidade? filters=trim
    text estado? filters=trim
    bool padrao?
    int cliente_id? {
      table = "CLIENTE"
    }
  }

  stack {
    api.request {
      url = "https://x8ki-letl-twmt.n7.xano.io/api:9mPF0785/upsertCEP"
      method = "POST"
      params = {
        cep   : $input.cep
        cidade: $input.cidade
        estado: $input.estado
      }
    
      headers = ["Content-type: application/json"]
    } as $api1
  
    api.request {
      url = "https://x8ki-letl-twmt.n7.xano.io/api:vXOkXuU3/endereco"
      method = "POST"
      params = {
          "logradouro": $input.logradouro,
          "número": $input.numero,
          "complemento": $input.complemento,
          "referencia": $input.referencia,
          "padrao": $input.padrao,
          "cliente_id": $input.cliente_id,
          "cep_id": $var.api1.response.result.id
      }
    
      headers = ["Content-Type: application/json"]
    } as $api2
  }

  response = ```
    {
        "logradouro": $var.api2.response.result.logradouro,
        "número": $var.api2.response.result.numero,
        "complemento": $var.api2.response.result.complemento,
        "referencia": $var.api2.response.result.referencia,
        "padrao": $var.api2.response.result.padrao,
        "cliente_id": $var.api2.response.result.cliente_id,
        "cep": {
        "cep_id": $var.api1.response.result.id,
        "cidade": $var.api2.response.result.cidade,
        "estado": $var.api2.response.result.estado,
    }
    ```
  guid = "V4P_70o69d2ETl4kvmH8ywPTiMc"
}