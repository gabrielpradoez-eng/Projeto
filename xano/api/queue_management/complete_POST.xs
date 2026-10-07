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
    // 1. Validar se a senha está sendo atendida
    db.get senhas {
      field_name = "id"
      field_value = $input.senha_id
    } as $senha
  
    precondition ($senha.status == "chamado") {
      error_type = "inputerror"
      error = "Esta senha não está em atendimento ou já foi finalizada."
    }
  
    // 2. Localizar o atendimento vinculado
    db.query atendimentos {
      where = $db.atendimentos.senha_id == $input.senha_id
      sort = {id: "desc"}
      return = {type: "single"}
    } as $atendimento
  
    // 3. Finalizar atômicamente
    db.transaction {
      stack {
        // Atualizar status da senha
        db.edit senhas {
          field_name = "id"
          field_value = $input.senha_id
          data = {status: "concluido", concluido_at: "now"}
        } as $senha_finalizada
      
        // Atualizar fim do atendimento
        db.edit atendimentos {
          field_name = "id"
          field_value = $atendimento.id
          data = {ended_at: "now"}
        } as $atendimento_finalizado

        db.query rastreamentos_senha {
          where = $db.rastreamentos_senha.senha_id == $input.senha_id && $db.rastreamentos_senha.revogada_at == null
          return = {type: "list"}
        } as $rastreamentos

        foreach ($rastreamentos.items) {
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