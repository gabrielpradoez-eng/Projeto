// Add SOLCANCELAMENTO record
query solcancelamento verb=POST {
  api_group = "CRUD_APIS_BASICO"

  input {
    dblink {
      table = "SOLCANCELAMENTO"
    }
  }

  stack {
    db.add SOLCANCELAMENTO {
      enforce_hidden_fields = false
      data = {
        created_at               : "now"
        motivo                   : $input.motivo
        pedido_id                : $input.pedido_id
        status_solcancelamento_id: $input.status_solcancelamento_id
      }
    } as $model
  }

  response = $model
  guid = "ZiOkOeq9qMBoWWEMQrS4YclICik"
}