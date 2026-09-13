// Query all PEDIDO records
query pedido verb=GET {
  api_group = "APIsCustom2"

  input {
  }

  stack {
    db.query PEDIDO {
      return = {type: "list"}
    } as $PEDIDO1
  }

  response = $pedido
  guid = "M__Y4XBrgoLS6A-hCEu4MUujKn0"
}