// Vincula uma conta de cliente existente à operação. Nunca recebe ou retorna senhas.
query "admin/attendants" verb=POST {
  api_group = "Queue Management"
  auth = "usuarios"

  input {
    email email filters=trim|lower
    int estabelecimento_id
    text destino_label filters=trim|min:1|max:80
  }

  stack {
    db.get usuarios {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "role", "estabelecimento_id"]
    } as $actor
    precondition ($actor != null && $actor.role == "admin") {
      error_type = "accessdenied"
      error = "Acesso restrito a administradores."
    }
    precondition (($actor.estabelecimento_id == null) || ($actor.estabelecimento_id == 0) || ($actor.estabelecimento_id == $input.estabelecimento_id)) {
      error_type = "accessdenied"
      error = "Estabelecimento fora do escopo autorizado."
    }
    db.get estabelecimentos {
      field_name = "id"
      field_value = $input.estabelecimento_id
    } as $site
    precondition ($site != null) {
      error_type = "inputerror"
      error = "Estabelecimento inválido."
    }
    db.transaction {
      stack {
        db.get usuarios {
          field_name = "email"
          field_value = $input.email
          output = ["id", "name", "role", "estabelecimento_id"]
        } as $candidate
        precondition ($candidate != null && $candidate.role == "usuario") {
          error_type = "inputerror"
          error = "Cadastre primeiro uma conta de cliente elegível."
        }
        precondition (($candidate.estabelecimento_id == null) || ($candidate.estabelecimento_id == 0) || ($candidate.estabelecimento_id == $site.id)) {
          error_type = "inputerror"
          error = "Conta vinculada a outro estabelecimento."
        }
        db.query atendentes {
          where = $db.atendentes.usuario_id == $candidate.id
          return = {type: "single"}
        } as $existing
        precondition ($existing == null) {
          error_type = "inputerror"
          error = "A conta já possui vínculo de atendimento."
        }
        db.add atendentes {
          data = {usuario_id: $candidate.id, estabelecimento_id: $site.id, destino_label: $input.destino_label, ativo: true}
        } as $staff
        db.edit usuarios {
          field_name = "id"
          field_value = $candidate.id
          data = {role: "atendente", estabelecimento_id: $site.id}
        } as $updated
      }
    }
  }
  response = {id: $updated.id, role: "atendente", estabelecimento_id: $site.id}
}
