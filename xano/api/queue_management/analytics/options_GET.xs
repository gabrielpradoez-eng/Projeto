// Retorna opções de filtro analítico limitadas ao escopo do administrador
query "analytics/options" verb=GET {
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

    precondition ($actor.role == "admin") {
      error_type = "accessdenied"
      error = "Acesso restrito a administradores."
    }

    db.query estabelecimentos {
      where = (($actor.estabelecimento_id == null) || ($actor.estabelecimento_id == 0)) || ($db.estabelecimentos.id == $actor.estabelecimento_id)
      sort = {nome: "asc"}
      return = {type: "list"}
    } as $estabelecimentos

    var $estabelecimentos_options {
      value = []
    }

    var $filas_options {
      value = []
    }

    foreach ($estabelecimentos) {
      each as $estabelecimento {
        array.push $estabelecimentos_options {
          value = {
            id  : $estabelecimento.id
            nome: $estabelecimento.nome
          }
        }

        db.query servicos {
          where = $db.servicos.estabelecimento_id == $estabelecimento.id
          sort = {nome: "asc"}
          return = {type: "list"}
        } as $servicos

        foreach ($servicos) {
          each as $servico {
            db.query filas {
              where = $db.filas.servico_id == $servico.id
              sort = {nome: "asc"}
              return = {type: "list"}
            } as $filas

            foreach ($filas) {
              each as $fila {
                array.push $filas_options {
                  value = {
                    estabelecimento_id  : $estabelecimento.id
                    estabelecimento_nome: $estabelecimento.nome
                    servico_id           : $servico.id
                    servico_nome         : $servico.nome
                    fila_id              : $fila.id
                    fila_nome            : $fila.nome
                  }
                }
              }
            }
          }
        }
      }
    }
  }

  response = {
    estabelecimentos: $estabelecimentos_options
    filas            : $filas_options
  }
}