// Delete PEDIDO record.
query "pedido/{pedido_id}" verb=DELETE {
  api_group = "APIsCustom2"

  input {
    int pedido_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.pedido_id
    }
  }

  response = null
  guid = "2UykrP5aMwJIblECOeEF2Igz_u8"
}