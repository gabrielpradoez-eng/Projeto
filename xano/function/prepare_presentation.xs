// Rotina interna e manual. Sem endpoint publico. Nao cria contas ou credenciais.
function prepare_presentation {
  input { bool apply?=false }
  stack {
    db.get estabelecimentos { field_name = "id"
      field_value = 1 } as $site
    precondition ($site != null && $site.nome == "Central de Atendimento — Demonstração") { error_type = "inputerror"
      error = "Rotina exclusiva do estabelecimento de demonstracao." }
    db.get usuarios { field_name = "id"
      field_value = 4
      output = ["id", "name", "role", "estabelecimento_id"] } as $tech
    precondition ($tech.role == "totem" && $tech.estabelecimento_id == 1) { error_type = "inputerror"
      error = "Conta tecnica fora do escopo esperado." }
    db.get atendentes { field_name = "id"
      field_value = 1 } as $staff
    precondition ($staff.usuario_id == 2 && $staff.estabelecimento_id == 1 && $staff.ativo) { error_type = "inputerror"
      error = "Atendente de demonstracao indisponivel." }
    db.get servicos { field_name = "id"
      field_value = 1 } as $original_service
    precondition ($original_service.estabelecimento_id == 1 && ($original_service.nome == "[TESTE] Atendimento geral" || $original_service.nome == "Atendimento geral")) { error_type = "inputerror"
      error = "Servico original fora do escopo esperado." }
    db.get filas { field_name = "id"
      field_value = 1 } as $original_queue
    precondition ($original_queue.servico_id == 1) { error_type = "inputerror"
      error = "Fila original fora do escopo esperado." }
    var $services { value = [{"nome":"Atendimento geral","fila":"Fila principal","minutos":10},{"nome":"Suporte técnico","fila":"Fila de suporte","minutos":15},{"nome":"Retirada de documentos","fila":"Fila de retirada","minutos":5},{"nome":"Informações e cadastro","fila":"Fila de informações","minutos":8}] }
    var $samples { value = [{"key":"demo-apresentacao-20261029-01","servico":"Atendimento geral","created":1792846800000,"called":1792846980000,"ended":1792847580000},{"key":"demo-apresentacao-20261029-02","servico":"Suporte técnico","created":1792850400000,"called":1792850640000,"ended":1792851540000},{"key":"demo-apresentacao-20261029-03","servico":"Retirada de documentos","created":1792933200000,"called":1792933500000,"ended":1792933800000},{"key":"demo-apresentacao-20261029-04","servico":"Informações e cadastro","created":1792936800000,"called":1792937160000,"ended":1792937640000},{"key":"demo-apresentacao-20261029-05","servico":"Atendimento geral","created":1793019600000,"called":1793020020000,"ended":1793020620000},{"key":"demo-apresentacao-20261029-06","servico":"Suporte técnico","created":1793023200000,"called":1793023380000,"ended":1793024280000},{"key":"demo-apresentacao-20261029-07","servico":"Retirada de documentos","created":1793106000000,"called":1793106240000,"ended":1793106540000},{"key":"demo-apresentacao-20261029-08","servico":"Informações e cadastro","created":1793109600000,"called":1793109900000,"ended":1793110380000},{"key":"demo-apresentacao-20261029-09","servico":"Atendimento geral","created":1793192400000,"called":1793192760000,"ended":1793193360000},{"key":"demo-apresentacao-20261029-10","servico":"Suporte técnico","created":1793196000000,"called":1793196420000,"ended":1793197320000},{"key":"demo-apresentacao-20261029-11","servico":"Retirada de documentos","created":1793278800000,"called":1793278980000,"ended":1793279280000},{"key":"demo-apresentacao-20261029-12","servico":"Informações e cadastro","created":1793282400000,"called":1793282640000,"ended":1793283120000}] }
    var $fixtures { value = [{"id":1,"created":1793030400000,"called":1793030700000,"ended":1793031060000},{"id":2,"created":1793031300000,"called":1793031600000,"ended":1793031960000},{"id":3,"created":1793032200000,"called":1793032500000,"ended":1793032860000},{"id":4,"created":1793033100000,"called":1793033400000,"ended":1793033760000}] }
    var $created_items { value = [] }
    conditional {
      if ($input.apply) {
        db.transaction {
          stack {
            db.edit servicos { field_name = "id"
      field_value = 1
      data = {nome: "Atendimento geral", tempo_estimado: 10} } as $service_renamed
            db.edit filas { field_name = "id"
      field_value = 1
      data = {nome: "Fila principal"} } as $queue_renamed
            db.edit atendentes { field_name = "id"
      field_value = 1
      data = {destino_label: "Guichê 01"} } as $staff_renamed
            db.edit usuarios { field_name = "id"
      field_value = 4
      data = {name: "Totem de autoatendimento"} } as $tech_renamed
            foreach ($services) {
              each as $item {
                db.query servicos { where = $db.servicos.estabelecimento_id == 1 && $db.servicos.nome == $item.nome
      return = {type: "single"} } as $existing_service
                conditional { if ($existing_service == null) { db.add servicos {
      data = {estabelecimento_id: 1, nome: $item.nome, tempo_estimado: $item.minutos} } as $new_service } }
                db.query servicos { where = $db.servicos.estabelecimento_id == 1 && $db.servicos.nome == $item.nome
      return = {type: "single"} } as $current_service
                db.query filas { where = $db.filas.servico_id == $current_service.id && $db.filas.nome == $item.fila
      return = {type: "single"} } as $existing_queue
                conditional { if ($existing_queue == null) { db.add filas {
      data = {servico_id: $current_service.id, nome: $item.fila, status: "aberta"} } as $new_queue } }
              }
            }
            foreach ($fixtures) {
              each as $fixture {
                db.get senhas { field_name = "id"
      field_value = $fixture.id } as $old_ticket
                conditional {
                  if ($old_ticket != null && $old_ticket.fila_id == 1 && $old_ticket.status == "concluido") {
                    db.edit senhas { field_name = "id"
      field_value = $fixture.id
      data = {created_at: $fixture.created, chamado_at: $fixture.called, concluido_at: $fixture.ended} } as $normalized_ticket
                    db.query atendimentos { where = $db.atendimentos.senha_id == $fixture.id && $db.atendimentos.estabelecimento_id == 1
      return = {type: "single"} } as $old_service
                    conditional { if ($old_service != null) { db.edit atendimentos { field_name = "id"
      field_value = $old_service.id
      data = {created_at: $fixture.called, started_at: $fixture.called, ended_at: $fixture.ended, destino_label: "Guichê 01"} } as $normalized_service } }
                  }
                }
              }
            }
            foreach ($samples) {
              each as $sample {
                db.get atendimentos { field_name = "display_event_key"
      field_value = $sample.key } as $existing_call
                conditional {
                  if ($existing_call == null) {
                    db.query servicos { where = $db.servicos.estabelecimento_id == 1 && $db.servicos.nome == $sample.servico
      return = {type: "single"} } as $sample_service
                    db.query filas { where = $db.filas.servico_id == $sample_service.id
      sort = {id: "asc"}
      return = {type: "single"} } as $sample_queue
                    db.query senhas { where = $db.senhas.fila_id == $sample_queue.id
      sort = {numero: "desc"}
      return = {type: "single"} } as $last_ticket
                    var $next_number { value = ($last_ticket.numero ?? 0) + 1 }
                    db.add senhas {
      data = {created_at: $sample.created, fila_id: $sample_queue.id, usuario_id: 4, numero: $next_number, status: "concluido", chamado_at: $sample.called, concluido_at: $sample.ended} } as $demo_ticket
                    db.add atendimentos {
      data = {created_at: $sample.called, senha_id: $demo_ticket.id, atendente_id: 1, estabelecimento_id: 1, numero_senha: $demo_ticket.numero, destino_label: "Guichê 01", display_event_key: $sample.key, started_at: $sample.called, ended_at: $sample.ended} } as $demo_call
                    array.push $created_items { value = {senha_id: $demo_ticket.id, atendimento_id: $demo_call.id, servico: $sample.servico, numero: $demo_ticket.numero} }
                  }
                }
              }
            }
          }
        }
      }
    }
    db.query servicos { where = $db.servicos.estabelecimento_id == 1
      return = {type: "list"} } as $catalog
    db.query senhas {
      return = {type: "count"} } as $ticket_count
    db.query atendimentos { where = $db.atendimentos.estabelecimento_id == 1
      return = {type: "count"} } as $call_count
  }
  response = {applied: $input.apply, estabelecimento: $site.nome, catalogo: $catalog, senhas_total: $ticket_count, atendimentos_total: $call_count, criados: $created_items}
}