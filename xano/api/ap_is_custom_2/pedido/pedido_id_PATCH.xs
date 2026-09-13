// Edit PEDIDO record
query "pedido/{pedido_id}" verb=PATCH {
  api_group = "APIsCustom2"

  input {
    int pedido_id? filters=min:1
    dblink {
      table = ""
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch "" {
      field_name = "id"
      field_value = $input.pedido_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $pedido
  }

  response = $pedido
  guid = "T2dk-RM0Qiu2ECVR1HwyVeDmAR8"
}