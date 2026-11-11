// Emite uma senha vinculada ao cliente autenticado.
query "customer/issue" verb=POST {
  api_group = "Queue Management"
  auth = "usuarios"

  input {
    int fila_id {
      table = "filas"
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

    precondition ($actor.role == "usuario") {
      error_type = "accessdenied"
      error = "Acesso restrito a clientes."
    }

    db.query filas {
      join = {
        servico: {
          table: "servicos"
          where: $db.filas.servico_id == $db.servico.id
        }
      }
      where = $db.filas.id == $input.fila_id && $db.filas.status == "aberta" && ($actor.estabelecimento_id == null || $actor.estabelecimento_id == 0 || $db.servico.estabelecimento_id == $actor.estabelecimento_id)
      return = {type: "single"}
    } as $fila

    precondition ($fila != null) {
      error_type = "notfound"
      error = "Fila indisponível para esta conta."
    }

    security.create_uuid as $referencia

    db.transaction {
      stack {
        // Bloqueio comum por fila; releitura antes de alocar o numero.
        db.get filas {
          field_name = "id"
          field_value = $input.fila_id
          lock = true
        } as $locked_queue
        precondition ($locked_queue != null && $locked_queue.status == "aberta" && $locked_queue.servico_id == $fila.servico_id) {
          error_type = "inputerror"
          error = "A fila nao esta disponivel."
        }
        db.get servicos {
          field_name = "id"
          field_value = $locked_queue.servico_id
        } as $locked_service
        precondition ($locked_service != null && ($actor.estabelecimento_id == null || $actor.estabelecimento_id == 0 || $locked_service.estabelecimento_id == $actor.estabelecimento_id)) {
          error_type = "accessdenied"
          error = "Fila fora do escopo autorizado."
        }
        db.query senhas {
          where = $db.senhas.fila_id == $input.fila_id
          sort = {numero: "desc"}
          return = {type: "single"}
        } as $ultima_senha

        var $proximo_numero {
          value = ($ultima_senha.numero ?? 0) + 1
        }

        db.add senhas {
          data = {
            fila_id   : $input.fila_id
            usuario_id: $auth.id
            numero    : $proximo_numero
            status    : "aguardando"
          }
        } as $nova_senha

        db.add rastreamentos_senha {
          data = {
            senha_id      : $nova_senha.id
            referencia_hash: $referencia|sha256
            expira_at     : ($nova_senha.created_at|add_secs_to_timestamp:(86400|to_int))
          }
        } as $rastreamento
      }
    }

    function.run "Quick Start/log_event" {
      input = {
        user_id : $auth.id
        action  : "customer_issue_ticket"
        metadata: {senha_id: $nova_senha.id, fila_id: $input.fila_id, numero: $nova_senha.numero}
      }
    } as $log
  }

  response = {
    numero              : $nova_senha.numero
    status              : $nova_senha.status
    referencia_rastreamento: $referencia
    expira_at           : $rastreamento.expira_at
  }
}
