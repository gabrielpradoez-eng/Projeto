// Add TTOKENIZACAO record
query ttokenizacao verb=POST {
  api_group = "CRUD_APIS_BASICO"

  input {
    dblink {
      table = "TTOKENIZACAO"
    }
  }

  stack {
    db.add TTOKENIZACAO {
      enforce_hidden_fields = false
      data = {
        created_at            : "now"
        cliente_id            : $input.cliente_id
        det_cartao_encript    : $input.det_cartao_encript
        status_ttokenizacao_id: $input.status_ttokenizacao_id
      }
    } as $model
  }

  response = $model
  guid = "LekP0PUDwz4hG1qsMAziKbAKXV4"
}