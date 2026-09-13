// Add OE record
query oe verb=POST {
  api_group = "CRUD_APIS_BASICO"

  input {
    dblink {
      table = "OE"
    }
  }

  stack {
    db.add OE {
      enforce_hidden_fields = false
      data = {
        created_at  : "now"
        status_oe_id: $input.status_oe_id
        pedido_id   : $input.pedido_id
      }
    } as $model
  }

  response = $model
  guid = "lVtqv7iYimvsVZS-ZjhP-YTJii4"
}