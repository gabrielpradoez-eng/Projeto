// Retorna relatório agregado de filas; cálculos e filtros permanecem no Xano
query "analytics/report" verb=POST {
  api_group = "Queue Management"
  auth = "usuarios"

  input {
    int estabelecimento_id {
      table = "estabelecimentos"
    }
    timestamp period_start
    timestamp period_end
    int servico_id? {
      table = "servicos"
    }
    int fila_id? {
      table = "filas"
    }
  }

  stack {
    precondition ($auth.role == "admin") {
      error_type = "accessdenied"
      error = "Acesso restrito a administradores."
    }

    precondition (($auth.estabelecimento_id == null) || ($auth.estabelecimento_id == $input.estabelecimento_id)) {
      error_type = "accessdenied"
      error = "Você não tem acesso a este estabelecimento."
    }

    precondition ($input.period_start < $input.period_end) {
      error_type = "inputerror"
      error = "O início do período deve ser anterior ao fim."
    }

    var $period_ms {
      value = ($input.period_end|to_ms) - ($input.period_start|to_ms)
    }

    precondition ($period_ms <= 2678400000) {
      error_type = "inputerror"
      error = "O período máximo do relatório é de 31 dias."
    }

    db.get estabelecimentos {
      field_name = "id"
      field_value = $input.estabelecimento_id
    } as $estabelecimento

    precondition ($estabelecimento != null) {
      error_type = "notfound"
      error = "Estabelecimento não encontrado."
    }

    db.query filas {
      join = {
        servico: {
          table: "servicos"
          where: ($db.filas.servico_id == $db.servicos.id)
        }
      }
      where = ($db.servicos.estabelecimento_id == $input.estabelecimento_id && ($input.servico_id == null || $db.filas.servico_id == $input.servico_id) && ($input.fila_id == null || $db.filas.id == $input.fila_id))
      sort = {nome: "asc"}
      return = {type: "list", paging: {page: 1, per_page: 101}}
    } as $filas

    precondition ($filas.items|count > 0) {
      error_type = "inputerror"
      error = "Não há filas disponíveis para os filtros selecionados."
    }

    precondition ($filas.items|count <= 100) {
      error_type = "inputerror"
      error = "Reduza os filtros para limitar o número de filas do relatório."
    }

    var $queue_metrics {
      value = []
    }

    foreach ($filas.items) {
      each as $fila {
        db.query senhas {
          where = ($db.senhas.fila_id == $fila.id && $db.senhas.created_at >= $input.period_start && $db.senhas.created_at < $input.period_end)
          return = {type: "count"}
        } as $issued_count

        db.query senhas {
          where = ($db.senhas.fila_id == $fila.id && $db.senhas.chamado_at >= $input.period_start && $db.senhas.chamado_at < $input.period_end)
          return = {type: "count"}
        } as $called_count

        db.query senhas {
          where = ($db.senhas.fila_id == $fila.id && $db.senhas.concluido_at >= $input.period_start && $db.senhas.concluido_at < $input.period_end)
          return = {type: "count"}
        } as $completed_event_count

        db.query senhas {
          where = ($db.senhas.fila_id == $fila.id && $db.senhas.created_at >= $input.period_start && $db.senhas.created_at < $input.period_end && $db.senhas.status == "aguardando")
          return = {type: "count"}
        } as $cohort_waiting

        db.query senhas {
          where = ($db.senhas.fila_id == $fila.id && $db.senhas.created_at >= $input.period_start && $db.senhas.created_at < $input.period_end && $db.senhas.status == "chamado")
          return = {type: "count"}
        } as $cohort_called

        db.query senhas {
          where = ($db.senhas.fila_id == $fila.id && $db.senhas.created_at >= $input.period_start && $db.senhas.created_at < $input.period_end && $db.senhas.status == "concluido")
          return = {type: "count"}
        } as $cohort_completed

        db.query senhas {
          where = ($db.senhas.fila_id == $fila.id && $db.senhas.created_at >= $input.period_start && $db.senhas.created_at < $input.period_end && $db.senhas.status == "cancelado")
          return = {type: "count"}
        } as $cohort_cancelled

        db.query senhas {
          where = ($db.senhas.fila_id == $fila.id && $db.senhas.chamado_at >= $input.period_start && $db.senhas.chamado_at < $input.period_end && $db.senhas.created_at != null)
          return = {type: "count"}
        } as $wait_sample_count

        precondition ($wait_sample_count <= 1000) {
          error_type = "inputerror"
          error = "O relatório excede o limite de amostras de espera; reduza o período ou filtre por fila."
        }

        db.query senhas {
          where = ($db.senhas.fila_id == $fila.id && $db.senhas.chamado_at >= $input.period_start && $db.senhas.chamado_at < $input.period_end && $db.senhas.created_at != null)
          sort = {chamado_at: "asc"}
          return = {type: "list", paging: {page: 1, per_page: 1000}}
        } as $wait_samples

        var $wait_total_ms {
          value = $wait_samples.items|reduce:(($$.chamado_at|to_ms) - ($$.created_at|to_ms)) + $result:0
        }

        db.query atendimentos {
          join = {
            senha: {
              table: "senhas"
              where: ($db.atendimentos.senha_id == $db.senhas.id)
            }
          }
          where = ($db.atendimentos.estabelecimento_id == $input.estabelecimento_id && $db.atendimentos.ended_at >= $input.period_start && $db.atendimentos.ended_at < $input.period_end && $db.atendimentos.started_at != null && $db.senhas.fila_id == $fila.id)
          return = {type: "count"}
        } as $service_sample_count

        precondition ($service_sample_count <= 1000) {
          error_type = "inputerror"
          error = "O relatório excede o limite de amostras de duração; reduza o período ou filtre por fila."
        }

        db.query atendimentos {
          join = {
            senha: {
              table: "senhas"
              where: ($db.atendimentos.senha_id == $db.senhas.id)
            }
          }
          where = ($db.atendimentos.estabelecimento_id == $input.estabelecimento_id && $db.atendimentos.ended_at >= $input.period_start && $db.atendimentos.ended_at < $input.period_end && $db.atendimentos.started_at != null && $db.senhas.fila_id == $fila.id)
          sort = {ended_at: "asc"}
          return = {type: "list", paging: {page: 1, per_page: 1000}}
        } as $service_samples

        var $service_total_ms {
          value = $service_samples.items|reduce:(($$.ended_at|to_ms) - ($$.started_at|to_ms)) + $result:0
        }

        var $queue_wait_average_minutes {
          value = ($wait_sample_count > 0) ? (($wait_total_ms / $wait_sample_count / 60000)|round:1) : null
        }

        var $queue_service_average_minutes {
          value = ($service_sample_count > 0) ? (($service_total_ms / $service_sample_count / 60000)|round:1) : null
        }

        array.push $queue_metrics {
          value = {
            servico_nome          : $fila.servico.nome
            fila_nome             : $fila.nome
            emitidas              : $issued_count
            chamadas              : $called_count
            concluidas            : $completed_event_count
            coorte_aguardando     : $cohort_waiting
            coorte_chamado        : $cohort_called
            coorte_concluido      : $cohort_completed
            coorte_cancelado      : $cohort_cancelled
            espera_media_minutos  : $queue_wait_average_minutes
            espera_total_ms       : $wait_total_ms
            espera_amostras       : $wait_sample_count
            duracao_media_minutos : $queue_service_average_minutes
            duracao_total_ms      : $service_total_ms
            duracao_amostras      : $service_sample_count
          }
        }
      }
    }

    var $day_offsets {
      value = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
    }

    var $daily_series {
      value = []
    }

    foreach ($day_offsets) {
      each as $day_offset {
        var $bucket_start {
          value = $input.period_start|add_secs_to_timestamp:($day_offset * 86400)
        }

        var $next_bucket_start {
          value = $bucket_start|add_secs_to_timestamp:(86400|to_int)
        }

        var $bucket_end {
          value = ($next_bucket_start < $input.period_end) ? $next_bucket_start : $input.period_end
        }

        conditional {
          if ($bucket_start < $input.period_end) {
            db.query senhas {
              join = {
                fila: {
                  table: "filas"
                  where: ($db.senhas.fila_id == $db.filas.id)
                }
                servico: {
                  table: "servicos"
                  where: ($db.filas.servico_id == $db.servicos.id)
                }
              }
              where = ($db.servicos.estabelecimento_id == $input.estabelecimento_id && ($input.servico_id == null || $db.filas.servico_id == $input.servico_id) && ($input.fila_id == null || $db.filas.id == $input.fila_id) && $db.senhas.created_at >= $bucket_start && $db.senhas.created_at < $bucket_end)
              return = {type: "count"}
            } as $daily_issued

            db.query senhas {
              join = {
                fila: {
                  table: "filas"
                  where: ($db.senhas.fila_id == $db.filas.id)
                }
                servico: {
                  table: "servicos"
                  where: ($db.filas.servico_id == $db.servicos.id)
                }
              }
              where = ($db.servicos.estabelecimento_id == $input.estabelecimento_id && ($input.servico_id == null || $db.filas.servico_id == $input.servico_id) && ($input.fila_id == null || $db.filas.id == $input.fila_id) && $db.senhas.chamado_at >= $bucket_start && $db.senhas.chamado_at < $bucket_end)
              return = {type: "count"}
            } as $daily_called

            db.query senhas {
              join = {
                fila: {
                  table: "filas"
                  where: ($db.senhas.fila_id == $db.filas.id)
                }
                servico: {
                  table: "servicos"
                  where: ($db.filas.servico_id == $db.servicos.id)
                }
              }
              where = ($db.servicos.estabelecimento_id == $input.estabelecimento_id && ($input.servico_id == null || $db.filas.servico_id == $input.servico_id) && ($input.fila_id == null || $db.filas.id == $input.fila_id) && $db.senhas.concluido_at >= $bucket_start && $db.senhas.concluido_at < $bucket_end)
              return = {type: "count"}
            } as $daily_completed

            array.push $daily_series {
              value = {
                bucket_start: $bucket_start
                emitidas    : $daily_issued
                chamadas    : $daily_called
                concluidas  : $daily_completed
              }
            }
          }
        }
      }
    }

    var $total_issued {
      value = $queue_metrics|reduce:$$.emitidas + $result:0
    }

    var $total_called {
      value = $queue_metrics|reduce:$$.chamadas + $result:0
    }

    var $total_completed {
      value = $queue_metrics|reduce:$$.concluidas + $result:0
    }

    var $cohort_waiting_total {
      value = $queue_metrics|reduce:$$.coorte_aguardando + $result:0
    }

    var $cohort_called_total {
      value = $queue_metrics|reduce:$$.coorte_chamado + $result:0
    }

    var $cohort_completed_total {
      value = $queue_metrics|reduce:$$.coorte_concluido + $result:0
    }

    var $cohort_cancelled_total {
      value = $queue_metrics|reduce:$$.coorte_cancelado + $result:0
    }

    var $total_wait_ms {
      value = $queue_metrics|reduce:$$.espera_total_ms + $result:0
    }

    var $total_wait_samples {
      value = $queue_metrics|reduce:$$.espera_amostras + $result:0
    }

    var $total_service_ms {
      value = $queue_metrics|reduce:$$.duracao_total_ms + $result:0
    }

    var $total_service_samples {
      value = $queue_metrics|reduce:$$.duracao_amostras + $result:0
    }

    var $wait_average_minutes {
      value = ($total_wait_samples > 0) ? (($total_wait_ms / $total_wait_samples / 60000)|round:1) : null
    }

    var $service_average_minutes {
      value = ($total_service_samples > 0) ? (($total_service_ms / $total_service_samples / 60000)|round:1) : null
    }

    var $completion_rate {
      value = ($total_issued > 0) ? (($cohort_completed_total / $total_issued * 100)|round:1) : null
    }
  }

  response = {
    generated_at: now
    filters     : {
      estabelecimento_id: $input.estabelecimento_id
      period_start      : $input.period_start
      period_end        : $input.period_end
      servico_id        : $input.servico_id
      fila_id           : $input.fila_id
    }
    queues      : $filas.items|map:{
      estabelecimento_id: $input.estabelecimento_id
      servico_id        : $$.servico_id
      servico_nome      : $$.servico.nome
      fila_id           : $$.id
      fila_nome         : $$.nome
    }
    summary     : {
      emitidas                : $total_issued
      chamadas                : $total_called
      concluidas              : $total_completed
      espera_media_minutos    : $wait_average_minutes
      espera_amostras         : $total_wait_samples
      duracao_media_minutos   : $service_average_minutes
      duracao_amostras        : $total_service_samples
      coorte_status           : {
        aguardando: $cohort_waiting_total
        chamado   : $cohort_called_total
        concluido : $cohort_completed_total
        cancelado : $cohort_cancelled_total
      }
      taxa_conclusao_coorte_pct: $completion_rate
    }
    daily       : $daily_series
    breakdown   : $queue_metrics|map:{
      servico_nome        : $$.servico_nome
      fila_nome           : $$.fila_nome
      emitidas            : $$.emitidas
      chamadas            : $$.chamadas
      concluidas          : $$.concluidas
      espera_media_minutos: $$.espera_media_minutos
      espera_amostras     : $$.espera_amostras
      duracao_media_minutos: $$.duracao_media_minutos
      duracao_amostras    : $$.duracao_amostras
      coorte_aguardando   : $$.coorte_aguardando
      coorte_chamado      : $$.coorte_chamado
      coorte_concluido    : $$.coorte_concluido
      coorte_cancelado    : $$.coorte_cancelado
    }
  }
}