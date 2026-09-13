// Update TRANSACAO record
query "transacao/{transacao_id}" verb=PUT {
  api_group = "CRUD_APIS_BASICO"

  input {
    int transacao_id? filters=min:1
    dblink {
      table = "TRANSACAO"
    }
  }

  stack {
    db.edit TRANSACAO {
      field_name = "id"
      field_value = $input.transacao_id
      enforce_hidden_fields = false
      data = {
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
  guid = "PWldzqNtsheQxjqeh6cLKKnXSZ0"
}