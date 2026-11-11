// Lê ou envia mensagens para o atendimento ativo e autorizado.
query chat verb=POST {
  api_group = "Queue Management"
  auth = "usuarios"

  input {
    int senha_id?=0
    text mensagem?="" filters=trim|max:500
  }

  stack {
    db.get usuarios {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "role", "estabelecimento_id"]
    } as $actor
    precondition ($actor != null && ($actor.role == "usuario" || $actor.role == "atendente")) {
      error_type = "accessdenied"
      error = "Conversa indisponível para esta conta."
    }
    precondition ($input.senha_id > 0 || ($input.senha_id == 0 && $actor.role == "usuario" && $input.mensagem == "")) {
      error_type = "inputerror"
      error = "Selecione um atendimento ativo."
    }
    db.query senhas {
      where = $db.senhas.status == "chamado" && (($input.senha_id > 0 && $db.senhas.id == $input.senha_id) || ($input.senha_id == 0 && $db.senhas.usuario_id == $auth.id)) && ($actor.role == "atendente" || $db.senhas.usuario_id == $auth.id)
      sort = {chamado_at: "desc", id: "desc"}
      return = {type: "single"}
    } as $senha

    precondition ($senha != null || $input.senha_id == 0) {
      error_type = "notfound"
      error = "Conversa indisponível."
    }

    conditional {
      if ($senha != null) {
        db.transaction {
          stack {
            // Usa a mesma ordem de bloqueio de call_next e complete.
            db.get filas {
              field_name = "id"
              field_value = $senha.fila_id
              lock = true
            } as $fila
            db.get senhas {
              field_name = "id"
              field_value = $senha.id
            } as $atual
            precondition ($fila != null && $atual != null && $atual.fila_id == $fila.id && $atual.status == "chamado") {
              error_type = "notfound"
              error = "Conversa indisponível."
            }
            db.query atendimentos {
              where = $db.atendimentos.senha_id == $atual.id && ($db.atendimentos.ended_at == null || $db.atendimentos.ended_at == 0)
              sort = {id: "desc"}
              return = {type: "single"}
            } as $atendimento
            precondition ($atendimento != null) {
              error_type = "notfound"
              error = "Conversa indisponível."
            }
            db.get atendentes {
              field_name = "id"
              field_value = $atendimento.atendente_id
            } as $atendente
            db.get usuarios {
              field_name = "id"
              field_value = $atual.usuario_id
              output = ["id", "role"]
            } as $cliente
            precondition ($cliente != null && $cliente.role == "usuario" && $atendente != null && $atendente.ativo && $atendente.estabelecimento_id == $atendimento.estabelecimento_id) {
              error_type = "notfound"
              error = "Conversa indisponível."
            }
            precondition (($actor.role == "usuario" && $atual.usuario_id == $auth.id) || ($actor.role == "atendente" && $atendente.usuario_id == $auth.id)) {
              error_type = "accessdenied"
              error = "Conversa indisponível."
            }

            conditional {
              if ($input.mensagem != "") {
                db.add mensagens_atendimento {
                  data = {
                    atendimento_id: $atendimento.id
                    remetente_id: $auth.id
                    mensagem: $input.mensagem
                  }
                } as $nova_mensagem
              }
            }
            db.query mensagens_atendimento {
              where = $db.mensagens_atendimento.atendimento_id == $atendimento.id
              sort = {id: "desc"}
              return = {type: "list", paging: {page: 1, per_page: 50}}
              output = ["id", "created_at", "remetente_id", "mensagem"]
            } as $recentes
          }
        }
      }
    }
  }
  response = {
    atendimento: ($senha != null) ? {senha_id: $senha.id, numero: $senha.numero, guiche: $atendimento.destino_label} : null
    mensagens: ($senha != null) ? $recentes.items : []
  }
}
