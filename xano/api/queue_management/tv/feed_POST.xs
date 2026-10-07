// Snapshot público mínimo das chamadas de um display autorizado
query "tv/feed" verb=POST {
  api_group = "Queue Management"

  input {
    text credential
  }

  stack {
    var $credential_hash {
      value = $input.credential|sha256
    }

    db.get tv_displays {
      field_name = "credential_hash"
      field_value = $credential_hash
    } as $display

    precondition (($display != null) && ($display.ativo)) {
      error_type = "accessdenied"
      error = "Display não autorizado."
    }

    db.query atendimentos {
      where = $db.atendimentos.estabelecimento_id == $display.estabelecimento_id
      sort = {id: "desc"}
      return = {type: "single"}
    } as $chamada_atual

    var $historico {
      value = []
    }

    conditional {
      if ($chamada_atual != null) {
        db.query atendimentos {
          where = $db.atendimentos.estabelecimento_id == $display.estabelecimento_id && $db.atendimentos.id != $chamada_atual.id
          sort = {id: "desc"}
          return = {type: "list", paging: {page: 1, per_page: 5}}
        } as $chamadas_recentes

        foreach ($chamadas_recentes.items) {
          each as $chamada {
            array.push $historico {
              value = {
                event_key : $chamada.display_event_key
                numero    : $chamada.numero_senha
                destino   : $chamada.destino_label
                chamado_at: $chamada.started_at
              }
            }
          }
        }
      }
    }
  }

  response = {
    current_call: ($chamada_atual != null) ? {
      event_key : $chamada_atual.display_event_key
      numero    : $chamada_atual.numero_senha
      destino   : $chamada_atual.destino_label
      chamado_at: $chamada_atual.started_at
    } : null
    history    : $historico
    snapshot_at: now
  }
}