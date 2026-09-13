// Add PEDIDO record
query pedido verb=POST {
  api_group = "APIsCustom2"

  input {
    dblink {
      table = ""
    }
  }

  stack {
    db.add "" {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $pedido
  }

  response = $pedido
  guid = "7CFK_gDj-SZxkvJfAYREEaPp-Ac"
}