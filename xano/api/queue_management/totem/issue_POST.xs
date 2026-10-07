// Emite uma senha por um Totem autorizado e cria uma referência segura de acompanhamento
query "totem/issue" verb=POST {
  api_group = "Queue Management"
  auth = "usuarios"

  input {
    int fila_id {
      table = "filas"
    }
  }

  stack {
    precondition ($auth.role == "totem" && $auth.estabelecimento_id != null) {
      error_type = "accessdenied"
      error = "Acesso restrito ao Totem autorizado."
    }

    db.query filas {
      join = {
        servico: {
          table: "servicos"
          where: $db.filas.servico_id == $db.servicos.id
        }
      }
      where = $db.filas.id == $input.fila_id && $db.filas.status == "aberta" && $db.servicos.estabelecimento_id == $auth.estabelecimento_id
      return = {type: "single"}
    } as $fila

    precondition ($fila != null) {
      error_type = "notfound"
      error = "Fila indisponível para este Totem."
    }

    security.create_uuid as $referencia

    db.transaction {
      stack {
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
        action  : "totem_issue_ticket"
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