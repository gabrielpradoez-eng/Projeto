// Lista somente as filas abertas do estabelecimento vinculado ao usuário Totem
query "totem/queues" verb=GET {
  api_group = "Queue Management"
  auth = "usuarios"

  input {
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

    precondition ($actor.role == "totem") {
      error_type = "accessdenied"
      error = "Acesso restrito ao Totem autorizado."
    }

    precondition ($actor.estabelecimento_id != null) {
      error_type = "accessdenied"
      error = "Totem sem estabelecimento autorizado."
    }

    db.query filas {
      join = {
        servico: {
          table: "servicos"
          where: $db.filas.servico_id == $db.servico.id
        }
      }
      where = $db.filas.status == "aberta" && $db.servico.estabelecimento_id == $actor.estabelecimento_id
      return = {type: "list"}
      eval = {servico_nome: $db.servico.nome, tempo_estimado: $db.servico.tempo_estimado}
    } as $filas

    var $opcoes {
      value = []
    }

    foreach ($filas) {
      each as $fila {
        array.push $opcoes {
          value = {
            fila_id          : $fila.id
            fila_nome        : $fila.nome
            servico_id       : $fila.servico_id
            servico_nome     : $fila.servico_nome
            tempo_estimado_min: $fila.tempo_estimado
          }
        }
      }
    }
  }

  response = $opcoes
  guid = "Vf3U1M9jxB9kU_5rnHo-EiW9qDQ"
}