// Lista somente as filas abertas do estabelecimento vinculado ao usuário Totem
query "totem/queues" verb=GET {
  api_group = "Queue Management"
  auth = "usuarios"

  input {
  }

  stack {
    precondition ($auth.role == "totem") {
      error_type = "accessdenied"
      error = "Acesso restrito ao Totem autorizado."
    }

    precondition ($auth.estabelecimento_id != null) {
      error_type = "accessdenied"
      error = "Totem sem estabelecimento autorizado."
    }

    db.query filas {
      join = {
        servico: {
          table: "servicos"
          where: $db.filas.servico_id == $db.servicos.id
        }
      }
      where = $db.filas.status == "aberta" && $db.servicos.estabelecimento_id == $auth.estabelecimento_id
      return = {type: "list"}
    } as $filas

    var $opcoes {
      value = []
    }

    foreach ($filas.items) {
      each as $fila {
        array.push $opcoes {
          value = {
            fila_id          : $fila.id
            fila_nome        : $fila.nome
            servico_id       : $fila.servico_id
            servico_nome     : $fila.servico.nome
            tempo_estimado_min: $fila.servico.tempo_estimado
          }
        }
      }
    }
  }

  response = $opcoes
  guid = "Vf3U1M9jxB9kU_5rnHo-EiW9qDQ"
}