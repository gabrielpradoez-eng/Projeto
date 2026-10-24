// Consulta individual de uma senha por referência temporária
query tracking verb=POST {
  api_group = "Queue Management"

  input {
    text referencia
  }

  stack {
    var $referencia_hash {
      value = $input.referencia|sha256
    }

    db.get rastreamentos_senha {
      field_name = "referencia_hash"
      field_value = $referencia_hash
    } as $rastreamento

    precondition (($rastreamento != null) && ($rastreamento.revogada_at == null) && ($rastreamento.expira_at > now)) {
      error_type = "notfound"
      error = "Referência inválida ou acompanhamento encerrado."
    }

    db.get senhas {
      field_name = "id"
      field_value = $rastreamento.senha_id
    } as $senha

    precondition (($senha != null) && ($senha.status != "concluido")) {
      error_type = "notfound"
      error = "Referência inválida ou acompanhamento encerrado."
    }

    db.get filas {
      field_name = "id"
      field_value = $senha.fila_id
    } as $fila

    db.get servicos {
      field_name = "id"
      field_value = $fila.servico_id
    } as $servico

    db.query senhas {
      where = $db.senhas.fila_id == $senha.fila_id && $db.senhas.status == "aguardando" && $db.senhas.numero < $senha.numero
      return = {type: "count"}
    } as $aguardando_a_frente

    var $posicao {
      value = ($senha.status == "aguardando") ? ($aguardando_a_frente + 1) : null
    }

    var $tempo_estimado_min {
      value = ($senha.status == "aguardando") ? ($aguardando_a_frente * $servico.tempo_estimado) : null
    }
  }

  response = {
    numero              : $senha.numero
    fila                : $fila.nome
    servico             : $servico.nome
    status              : $senha.status
    posicao             : $posicao
    tempo_estimado_min  : $tempo_estimado_min
    atualizado_at       : now
  }
  guid = "3iC4CqZrL0USN_Q8Bf8glkjhmV4"
}