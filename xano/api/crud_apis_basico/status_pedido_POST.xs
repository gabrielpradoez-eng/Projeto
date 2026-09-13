// Add STATUS_PEDIDO record
query status_pedido verb=POST {
  api_group = "CRUD_APIS_BASICO"

  input {
    dblink {
      table = "STATUS_PEDIDO"
    }
  }

  stack {
    db.add STATUS_PEDIDO {
      enforce_hidden_fields = false
      data = {
        created_at : "now"
        status     : $input.status
        status_para: $input.status_para
      }
    } as $model
  }

  response = $model
  guid = "CbaXwpgOXzfjk4dfV6L4UxCdlWQ"
}