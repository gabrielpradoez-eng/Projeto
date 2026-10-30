// Finaliza o atendimento de uma senha
query complete verb=POST {
  api_group = "Queue Management"
  auth = "usuarios"

  input {
    int senha_id {
      table = "senhas"
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

    precondition ($actor.role == "atendente") {
      error_type = "accessdenied"
      error = "Apenas atendentes podem finalizar atendimentos."
    }

    db.get atendentes {
      field_name = "usuario_id"
      field_value = $auth.id
    } as $atendente

    precondition (($atendente != null) && ($atendente.ativo)) {
      error_type = "accessdenied"
      error = "Atendente inativo ou não cadastrado."
    }

    // 1. Validar se a senha está sendo atendida
    db.get senhas {
      field_name = "id"
      field_value = $input.senha_id
    } as $senha
  
    precondition (($senha != null) && ($senha.status == "chamado")) {
      error_type = "inputerror"
      error = "Esta senha não está em atendimento ou já foi finalizada."
    }
  
    // 2. Localizar o atendimento vinculado
    db.query atendimentos {
      where = $db.atendimentos.senha_id == $input.senha_id
      sort = {id: "desc"}
      return = {type: "single"}
    } as $atendimento
  
    precondition (($atendimento != null) && ($atendimento.atendente_id == $atendente.id) && ($atendimento.estabelecimento_id == $atendente.estabelecimento_id) && (($atendimento.ended_at == null) || ($atendimento.ended_at == 0))) {
      error_type = "accessdenied"
      error = "Você não pode finalizar este atendimento."
    }

    // 3. Finalizar atômicamente
    db.transaction {
      stack {
        db.get filas {
          field_name = "id"
          field_value = $senha.fila_id
          lock = true
        } as $locked_queue
        db.get senhas {
          field_name = "id"
          field_value = $input.senha_id
        } as $current_senha
        precondition ($locked_queue != null && $current_senha != null && $current_senha.fila_id == $locked_queue.id && $current_senha.status == "chamado") {
          error_type = "inputerror"
          error = "Esta senha ja nao esta em atendimento."
        }
        db.query atendimentos {
          where = $db.atendimentos.senha_id == $input.senha_id
          sort = {id: "desc"}
          return = {type: "single"}
        } as $current_atendimento
        precondition ($current_atendimento != null && $current_atendimento.atendente_id == $atendente.id && $current_atendimento.estabelecimento_id == $atendente.estabelecimento_id && ($current_atendimento.ended_at == null || $current_atendimento.ended_at == 0)) {
          error_type = "accessdenied"
          error = "Este atendimento ja foi encerrado ou esta fora do escopo."
        }
        // Atualizar status da senha
        db.edit senhas {
          field_name = "id"
          field_value = $input.senha_id
          data = {status: "concluido", concluido_at: "now"}
        } as $senha_finalizada
      
        // Atualizar fim do atendimento
        db.edit atendimentos {
          field_name = "id"
          field_value = $current_atendimento.id
          data = {ended_at: "now"}
        } as $atendimento_finalizado

        db.query rastreamentos_senha {
          where = $db.rastreamentos_senha.senha_id == $input.senha_id && ($db.rastreamentos_senha.revogada_at == null || $db.rastreamentos_senha.revogada_at == 0)
          return = {type: "list"}
        } as $rastreamentos

        foreach ($rastreamentos) {
          each as $rastreamento {
            db.edit rastreamentos_senha {
              field_name = "id"
              field_value = $rastreamento.id
              data = {revogada_at: "now"}
            } as $rastreamento_revogado
          }
        }
      }
    }
  
    // 4. Registrar log
    function.run "Quick Start/log_event" {
      input = {
        user_id : $auth.id
        action  : "complete_service"
        metadata: {
        senha_id      : $input.senha_id
        atendimento_id: $atendimento.id
      }
      }
    } as $log
  }

  response = {
    senha      : $senha_finalizada
    atendimento: $atendimento_finalizado
  }

  guid = "RvtlT2o8GPWzBVJxRZlgnLv7KXg"
}