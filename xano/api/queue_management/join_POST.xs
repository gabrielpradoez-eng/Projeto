// Gera uma nova senha para o usuário em uma fila específica
query join verb=POST {
  api_group = "Queue Management"
  auth = "usuarios"

  input {
    int fila_id {
      table = "filas"
    }
  }

  stack {
    // Verificar se a fila existe e está aberta
    db.get filas {
      field_name = "id"
      field_value = $input.fila_id
    } as $fila
  
    precondition ($fila != null) {
      error_type = "notfound"
      error = "Fila não encontrada."
    }
  
    precondition ($fila.status == "aberta") {
      error_type = "inputerror"
      error = "Esta fila está fechada no momento."
    }
  
    // Gerar o próximo número de forma atômica
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
        db.query senhas {
          where = $db.senhas.fila_id == $input.fila_id
          sort = {numero: "desc"}
          return = {type: "single"}
        } as $last_senha
      
        var $next_num {
          value = ($last_senha.numero ?? 0) + 1
        }
      
        db.add senhas {
          data = {
            fila_id   : $input.fila_id
            usuario_id: $auth.id
            numero    : $next_num
            status    : "aguardando"
          }
        } as $nova_senha
      }
    }
  
    // Registrar log de evento
    function.run "Quick Start/log_event" {
      input = {
        user_id : $auth.id
        action  : "join_queue"
        metadata: {
        fila_id : $input.fila_id
        senha_id: $nova_senha.id
        numero  : $nova_senha.numero
      }
      }
    } as $log
  }

  response = $nova_senha
  guid = "aGMzjxlOtyot-DDC6lCqBKfPLEc"
}