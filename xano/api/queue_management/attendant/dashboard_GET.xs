// Retorna o painel de controle do atendente com as filas sob sua responsabilidade
query "attendant/dashboard" verb=GET {
  api_group = "Queue Management"
  auth = "usuarios"

  input {
  }

  stack {
    // 1. Identificar o atendente e seu estabelecimento
    db.get atendentes {
      field_name = "usuario_id"
      field_value = $auth.id
    } as $atendente
  
    precondition (($atendente != null) && ($atendente.ativo)) {
      error_type = "accessdenied"
      error = "Acesso restrito a atendentes ativos."
    }
  
    // 2. Buscar todas as filas do estabelecimento
    db.query filas {
      join = {
        servico: {
          table: "servicos"
          where: $db.filas.servico_id == $db.servicos.id
        }
      }
    
      where = $db.servicos.estabelecimento_id == $atendente.estabelecimento_id
      return = {type: "list"}
    } as $filas
  
    // 3. Complementar cada fila com contagens
    var $dashboard {
      value = []
    }
  
    foreach ($filas.items) {
      each as $fila {
        // Pessoas aguardando
        db.query senhas {
          where = $db.senhas.fila_id == $fila.id && $db.senhas.status == "aguardando"
          return = {type: "count"}
        } as $total_aguardando
      
        // Última senha chamada
        db.query senhas {
          where = $db.senhas.fila_id == $fila.id && $db.senhas.status == "chamado"
          sort = {chamado_at: "desc"}
          return = {type: "single"}
        } as $ultima_chamada
      
        array.push $dashboard {
          value = {
            id              : $fila.id
            nome            : $fila.nome
            servico_id      : $fila.servico_id
            status_fila     : $fila.status
            total_aguardando: $total_aguardando
            em_atendimento  : $ultima_chamada
          }
        }
      }
    }
  }

  response = $dashboard
  guid = "mljEpv6v-8XbbYqfZR0shSQMGJo"
}