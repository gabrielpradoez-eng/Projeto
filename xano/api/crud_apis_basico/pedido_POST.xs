// Add PEDIDO record
query pedido verb=POST {
  api_group = "CRUD_APIS_BASICO"

  input {
    dblink {
      table = "PEDIDO"
    }
  }

  stack {
    db.add PEDIDO {
      enforce_hidden_fields = false
      data = {
        created_at      : "now"
        total           : $input.total
        nfc_e           : $input.nfc_e
        cod_entrega     : $input.cod_entrega
        status_pedido_id: $input.status_pedido_id
        cliente_id      : $input.cliente_id
      }
    } as $model
  }

  response = $model
  guid = "oL8KTUhV2StyLn7vIxuo2-p5mzg"
}