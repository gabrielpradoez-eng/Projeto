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
    db.get usuarios {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "role", "estabelecimento_id"]
    } as $actor

    precondition ($actor != null) {
      error_type = "accessdenied"
      error = "Usuário autenticado não encontrado."
    }

    precondition ($actor.role == "admin") {
      error_type = "accessdenied"
      error = "Apenas administradores podem provisionar displays."
    }

    precondition (($actor.estabelecimento_id == null) || ($actor.estabelecimento_id == 0) || ($actor.estabelecimento_id == $input.estabelecimento_id)) {
      error_type = "accessdenied"
      error = "Você não tem acesso a este estabelecimento."
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