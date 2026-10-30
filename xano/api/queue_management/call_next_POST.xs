// Chama a próxima senha disponível na fila para atendimento
query call_next verb=POST {
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

    precondition ($actor.role == "atendente") {
      error_type = "accessdenied"
      error = "Acesso restrito a atendentes."
    }

    // 1. Validar se o usuário é um atendente ativo
    db.get atendentes {
      field_name = "usuario_id"
      field_value = $auth.id
    } as $atendente
  
    precondition (($atendente != null) && ($atendente.ativo)) {
      error_type = "accessdenied"
      error = "Apenas atendentes ativos podem chamar senhas."
    }
  
    // 2. Verificar se a fila pertence ao estabelecimento do atendente
    db.get filas {
      field_name = "id"
      field_value = $input.fila_id
    } as $fila
  
    precondition (($fila != null) && ($fila.status == "aberta")) {
      error_type = "notfound"
      error = "Fila inexistente ou fechada."
    }

    db.get servicos {
      field_name = "id"
      field_value = $fila.servico_id
    } as $servico
  
    precondition (($servico != null) && ($servico.estabelecimento_id == $atendente.estabelecimento_id)) {
      error_type = "accessdenied"
      error = "Você não tem permissão para atender nesta fila."
    }
  
    // 3. Buscar a próxima senha aguardando (menor número)
    db.query senhas {
      where = $db.senhas.fila_id == $input.fila_id && $db.senhas.status == "aguardando"
      sort = {numero: "asc"}
      return = {type: "single"}
    } as $proxima_senha
  
    precondition ($proxima_senha != null) {
      error_type = "notfound"
      error = "Não há senhas aguardando nesta fila."
    }

    security.create_uuid as $display_event_key
  
    // 4. Iniciar atendimento atômicamente
    db.transaction {
      stack {
        // Atualizar status da senha
        db.edit senhas {
          field_name = "id"
          field_value = $proxima_senha.id
          data = {status: "chamado", chamado_at: "now"}
        } as $senha_atualizada
      
        // Criar registro de atendimento
        db.add atendimentos {
          data = {
            senha_id    : $proxima_senha.id
            atendente_id: $atendente.id
            estabelecimento_id: $atendente.estabelecimento_id
            numero_senha: $senha_atualizada.numero
            destino_label: $atendente.destino_label ?? "Guichê não informado"
            display_event_key: $display_event_key
            started_at  : "now"
          }
        } as $atendimento
      }
    }
  
    // 5. Registrar log de evento
    function.run "Quick Start/log_event" {
      input = {
        user_id : $auth.id
        action  : "call_next"
        metadata: {
        senha_id      : $proxima_senha.id
        atendimento_id: $atendimento.id
      }
      }
    } as $log
  }

  response = {senha: $senha_atualizada, atendimento: $atendimento}
  guid = "mzf3CWBOTVg04-e5ijOiBJ9EOTM"
}