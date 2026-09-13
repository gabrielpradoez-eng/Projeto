// Add TRANSACAO record
query transacao verb=POST {
  api_group = "CRUD_APIS_BASICO"

  input {
    dblink {
      table = "TRANSACAO"
    }
  }

  stack {
    db.add TRANSACAO {
      enforce_hidden_fields = false
      data = {
        created_at        : "now"
        clienteassas      : $input.clienteassas
        idpayment         : $input.idpayment
        tipo              : $input.tipo
        valor             : $input.valor
        datavenc          : $input.datavenc
        descricao         : $input.descricao
        statustransacao_id: $input.statustransacao_id
      }
    } as $model
  }

  response = $model
  guid = "Z7O0oYZq0Ieag3dj9946EBa5DLE"
}