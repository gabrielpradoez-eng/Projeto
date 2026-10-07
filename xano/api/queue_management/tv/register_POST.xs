// Provisiona um display público e retorna sua credencial uma única vez
query "tv/register" verb=POST {
  api_group = "Queue Management"
  auth = "usuarios"

  input {
    int estabelecimento_id {
      table = "estabelecimentos"
    }
  }

  stack {
    precondition ($auth.role == "admin") {
      error_type = "accessdenied"
      error = "Apenas administradores podem provisionar displays."
    }

    db.get estabelecimentos {
      field_name = "id"
      field_value = $input.estabelecimento_id
    } as $estabelecimento

    precondition ($estabelecimento != null) {
      error_type = "notfound"
      error = "Estabelecimento não encontrado."
    }

    security.create_uuid as $credential

    db.add tv_displays {
      data = {
        estabelecimento_id: $estabelecimento.id
        credential_hash   : $credential|sha256
        ativo             : true
      }
    } as $display
  }

  response = {
    credential: $credential
    estabelecimento: $estabelecimento.nome
  }
}