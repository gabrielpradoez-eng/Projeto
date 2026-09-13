// Update OE record
query "oe/{oe_id}" verb=PUT {
  api_group = "CRUD_APIS_BASICO"

  input {
    int oe_id? filters=min:1
    dblink {
      table = "OE"
    }
  }

  stack {
    db.edit OE {
      field_name = "id"
      field_value = $input.oe_id
      enforce_hidden_fields = false
      data = {
        status_oe_id: $input.status_oe_id
        pedido_id   : $input.pedido_id
      }
    } as $model
  }

  response = $model
  guid = "StfcLc2P2xpgl24qQ7qSbhyYOZQ"
}