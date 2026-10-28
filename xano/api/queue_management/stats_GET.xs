// Retorna estatísticas em tempo real de uma fila específica
query stats verb=GET {
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

    precondition (($actor.role == "admin") || ($actor.role == "atendente")) {
      error_type = "accessdenied"
      error = "Acesso restrito a administradores e atendentes."
    }

    db.get filas {
      field_name = "id"
      field_value = $input.fila_id
    } as $fila

    precondition ($fila != null) {
      error_type = "notfound"
      error = "Fila não encontrada."
    }

    db.get servicos {
      field_name = "id"
      field_value = $fila.servico_id
    } as $servico

    precondition ($servico != null) {
      error_type = "notfound"
      error = "Serviço não encontrado."
    }

    precondition (($actor.role != "admin") || ($actor.estabelecimento_id == null) || ($actor.estabelecimento_id == $servico.estabelecimento_id)) {
      error_type = "accessdenied"
      error = "Você não tem acesso a esta fila."
    }

    db.get atendentes {
      field_name = "usuario_id"
      field_value = $auth.id
    } as $atendente

    precondition (($actor.role != "atendente") || (($atendente != null) && ($atendente.ativo) && ($atendente.estabelecimento_id == $servico.estabelecimento_id))) {
      error_type = "accessdenied"
      error = "Você não tem acesso a esta fila."
    }
  
    db.query senhas {
      where = $db.senhas.fila_id == $input.fila_id && $db.senhas.status == "aguardando"
      return = {type: "count"}
    } as $aguardando_count
  
    db.query senhas {
      where = $db.senhas.fila_id == $input.fila_id && $db.senhas.chamado_at != null
      sort = {chamado_at: "desc"}
      return = {type: "list", paging: {page: 1, per_page: 20}}
    } as $recentes
  
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