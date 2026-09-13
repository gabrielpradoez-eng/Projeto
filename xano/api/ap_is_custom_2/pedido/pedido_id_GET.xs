// Get PEDIDO record
query "pedido/{pedido_id}" verb=GET {
  api_group = "APIsCustom2"

  input {
    int pedido_id? filters=min:1
  }

  stack {
    db.get "" {
      field_name = "id"
      field_value = $input.pedido_id
    } as $pedido
  
    precondition ($pedido != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $pedido
  guid = "X6dIS-sQShdeuXm6HEDCfq8vnrU"
}