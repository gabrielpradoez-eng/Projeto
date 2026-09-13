// Retorna estatísticas em tempo real de uma fila específica
query stats verb=GET {
  api_group = "Queue Management"

  input {
    int fila_id {
      table = "filas"
    }
  }

  stack {
    // 1. Obter informações da fila
    db.get filas {
      field_name = "id"
      field_value = $input.fila_id
    } as $fila
  
    // 2. Contar pessoas aguardando
    db.query senhas {
      where = $db.senhas.fila_id == $input.fila_id && $db.senhas.status == "aguardando"
      return = {type: "count"}
    } as $aguardando_count
  
    // 3. Obter últimas 20 senhas chamadas para calcular tempo médio recente
    db.query senhas {
      where = $db.senhas.fila_id == $input.fila_id && $db.senhas.chamado_at != null
      sort = {chamado_at: "desc"}
      return = {type: "list", paging: {page: 1, per_page: 20}}
    } as $recentes
  
    // 4. Calcular tempo médio em minutos
    var $senhas_list {
      value = $recentes.items
    }
  
    var $total_ms {
      value = $senhas_list|reduce:(($$.chamado_at|to_ms) - ($$.created_at|to_ms)) + $result:0
    }
  
    var $count {
      value = $senhas_list|count
    }
  
    var $tempo_medio_minutos {
      value = ($count > 0) ? (($total_ms / $count / 60000)|round:1) : 0
    }
  }

  response = {
    fila                  : $fila.nome
    status                : $fila.status
    aguardando            : $aguardando_count
    tempo_medio_espera_min: $tempo_medio_minutos
  }

  guid = "Yr3XgbV7C7S9R-xZ6cPcbE96rJs"
}