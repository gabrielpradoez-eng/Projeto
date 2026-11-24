// Catálogo da instalação independente. Nunca criar rotas CRUD públicas.
query "admin/catalog" verb=POST {
  api_group = "Queue Management"
  auth = "usuarios"
  input {
    enum acao?=listar { values = ["listar", "salvar"] }
    int fila_id?=0
    int estabelecimento_id?=0
    text servico_nome? filters=trim|max:100
    text fila_nome? filters=trim|max:100
    int tempo_estimado?=10
    enum status?=aberta { values = ["aberta", "fechada"] }
  }
  stack {
    db.get usuarios {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "role", "estabelecimento_id"]
    } as $actor
    precondition ($actor != null && $actor.role == "admin") {
      error_type = "accessdenied"
      error = "Acesso restrito a administradores."
    }
    conditional {
      if ($input.acao == "salvar") {
        precondition ($input.servico_nome != null && $input.servico_nome != "" && $input.fila_nome != null && $input.fila_nome != "" && $input.tempo_estimado >= 1 && $input.tempo_estimado <= 1440 && $input.fila_id >= 0) {
          error_type = "inputerror"
          error = "Dados de serviço ou fila inválidos."
        }
        precondition ($actor.estabelecimento_id == null || $actor.estabelecimento_id == 0 || $actor.estabelecimento_id == $input.estabelecimento_id) {
          error_type = "accessdenied"
          error = "Estabelecimento fora do escopo."
        }
        db.transaction {
          stack {
            db.get estabelecimentos {
              field_name = "id"
              field_value = $input.estabelecimento_id
            } as $site
            precondition ($site != null) {
              error_type = "inputerror"
              error = "Estabelecimento indisponível."
            }
            conditional {
              if ($input.fila_id > 0) {
                db.get filas {
                  field_name = "id"
                  field_value = $input.fila_id
                  lock = true
                } as $queue
                precondition ($queue != null) {
                  error_type = "inputerror"
                  error = "Fila indisponível."
                }
                db.get servicos {
                  field_name = "id"
                  field_value = $queue.servico_id
                  lock = true
                } as $service
                precondition ($service != null && $service.estabelecimento_id == $site.id) {
                  error_type = "accessdenied"
                  error = "Fila fora do escopo."
                }
                db.edit servicos {
                  field_name = "id"
                  field_value = $service.id
                  data = {nome: $input.servico_nome, tempo_estimado: $input.tempo_estimado}
                } as $saved_service
                db.edit filas {
                  field_name = "id"
                  field_value = $queue.id
                  data = {nome: $input.fila_nome, status: $input.status}
                } as $saved_queue
              }
              else {
                db.add servicos {
                  data = {estabelecimento_id: $site.id, nome: $input.servico_nome, tempo_estimado: $input.tempo_estimado}
                } as $saved_service
                db.add filas {
                  data = {servico_id: $saved_service.id, nome: $input.fila_nome, status: $input.status}
                } as $saved_queue
              }
            }
          }
        }
      }
    }
    db.query estabelecimentos {
      where = $actor.estabelecimento_id == null || $actor.estabelecimento_id == 0 || $db.estabelecimentos.id == $actor.estabelecimento_id
      return = {type: "list"}
    } as $sites
    var $catalog { value = [] }
    foreach ($sites) {
      each as $item_site {
        db.query servicos {
          where = $db.servicos.estabelecimento_id == $item_site.id
          sort = {id: "asc"}
          return = {type: "list"}
        } as $services
        foreach ($services) {
          each as $item_service {
            db.query filas {
              where = $db.filas.servico_id == $item_service.id
              sort = {id: "asc"}
              return = {type: "list"}
            } as $queues
            foreach ($queues) {
              each as $item_queue {
                array.push $catalog {
                  value = {estabelecimento_id: $item_site.id, estabelecimento_nome: $item_site.nome, servico_id: $item_service.id, servico_nome: $item_service.nome, tempo_estimado: $item_service.tempo_estimado, fila_id: $item_queue.id, fila_nome: $item_queue.nome, status: $item_queue.status}
                }
              }
            }
          }
        }
      }
    }
  }
  response = {filas: $catalog}
}
