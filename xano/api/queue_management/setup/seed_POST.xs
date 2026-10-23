// Provisiona dados fixos de teste; mantenha desabilitado fora de workspace descartável
query "setup/seed" verb=POST {
  api_group = "Queue Management"

  input {
    text bootstrap_secret
    text admin_password filters=trim|min:8
  }

  stack {
    precondition ($env.$xano_environment == "test") {
      error_type = "accessdenied"
      error = "Provisionamento permitido somente em ambiente de teste."
    }
  
    precondition ($env.$seed_enabled == "true") {
      error_type = "accessdenied"
      error = "Provisionamento de teste desabilitado."
    }
  
    precondition (($env.$seed_secret != null) && ($input.bootstrap_secret == $env.$seed_secret)) {
      error_type = "accessdenied"
      error = "Autorização de provisionamento inválida."
    }
  
    db.query estabelecimentos {
      where = $db.estabelecimentos.nome == "Matriz"
      return = {type: "single"}
    } as $estabelecimento_existente
  
    conditional {
      if ($estabelecimento_existente == null) {
        db.add estabelecimentos {
          data = {nome: "Matriz", endereco: "Unidade de teste"}
        } as $novo_estabelecimento
      }
    }
  
    db.query estabelecimentos {
      where = $db.estabelecimentos.nome == "Matriz"
      return = {type: "single"}
    } as $estabelecimento
  
    db.query usuarios {
      where = $db.usuarios.email == "admin@filasmart.com"
      return = {type: "single"}
    } as $admin_existente
  
    conditional {
      if ($admin_existente == null) {
        db.add usuarios {
          data = {
            name    : "Administrador de Teste"
            email   : "admin@filasmart.com"
            password: $input.admin_password
            role    : "admin"
          }
        } as $novo_admin
      }
    }
  
    db.query usuarios {
      where = $db.usuarios.email == "admin@filasmart.com"
      return = {type: "single"}
    } as $admin
  
    precondition ($admin.role == "admin") {
      error_type = "inputerror"
      error = "A conta admin@filasmart.com já existe fora do fixture esperado."
    }
  
    security.create_uuid as $atendente1_password
    db.query usuarios {
      where = $db.usuarios.email == "atendente1@filasmart.com"
      return = {type: "single"}
    } as $atendente1_existente
  
    conditional {
      if ($atendente1_existente == null) {
        db.add usuarios {
          data = {
            name    : "Atendente 1"
            email   : "atendente1@filasmart.com"
            password: $atendente1_password
            role    : "atendente"
          }
        } as $novo_atendente1
      }
    }
  
    db.query usuarios {
      where = $db.usuarios.email == "atendente1@filasmart.com"
      return = {type: "single"}
    } as $atendente1
  
    precondition ($atendente1.role == "atendente") {
      error_type = "inputerror"
      error = "A conta atendente1@filasmart.com já existe fora do fixture esperado."
    }
  
    db.query atendentes {
      where = $db.atendentes.usuario_id == $atendente1.id
      return = {type: "single"}
    } as $registro_atendente1
  
    conditional {
      if ($registro_atendente1 == null) {
        db.add atendentes {
          data = {
            usuario_id        : $atendente1.id
            estabelecimento_id: $estabelecimento.id
            ativo             : true
          }
        } as $novo_registro_atendente1
      }
    }
  
    precondition (($registro_atendente1 == null) || (($registro_atendente1.estabelecimento_id == $estabelecimento.id) && $registro_atendente1.ativo)) {
      error_type = "inputerror"
      error = "O vínculo do atendente 1 conflita com o fixture esperado."
    }
  
    security.create_uuid as $atendente2_password
    db.query usuarios {
      where = $db.usuarios.email == "atendente2@filasmart.com"
      return = {type: "single"}
    } as $atendente2_existente
  
    conditional {
      if ($atendente2_existente == null) {
        db.add usuarios {
          data = {
            name    : "Atendente 2"
            email   : "atendente2@filasmart.com"
            password: $atendente2_password
            role    : "atendente"
          }
        } as $novo_atendente2
      }
    }
  
    db.query usuarios {
      where = $db.usuarios.email == "atendente2@filasmart.com"
      return = {type: "single"}
    } as $atendente2
  
    precondition ($atendente2.role == "atendente") {
      error_type = "inputerror"
      error = "A conta atendente2@filasmart.com já existe fora do fixture esperado."
    }
  
    db.query atendentes {
      where = $db.atendentes.usuario_id == $atendente2.id
      return = {type: "single"}
    } as $registro_atendente2
  
    conditional {
      if ($registro_atendente2 == null) {
        db.add atendentes {
          data = {
            usuario_id        : $atendente2.id
            estabelecimento_id: $estabelecimento.id
            ativo             : true
          }
        } as $novo_registro_atendente2
      }
    }
  
    precondition (($registro_atendente2 == null) || (($registro_atendente2.estabelecimento_id == $estabelecimento.id) && $registro_atendente2.ativo)) {
      error_type = "inputerror"
      error = "O vínculo do atendente 2 conflita com o fixture esperado."
    }
  
    db.query servicos {
      where = $db.servicos.estabelecimento_id == $estabelecimento.id && $db.servicos.nome == "Atendimento Geral"
      return = {type: "single"}
    } as $servico_geral_existente
  
    conditional {
      if ($servico_geral_existente == null) {
        db.add servicos {
          data = {
            estabelecimento_id: $estabelecimento.id
            nome              : "Atendimento Geral"
            tempo_estimado    : 10
          }
        } as $novo_servico_geral
      }
    }
  
    db.query servicos {
      where = $db.servicos.estabelecimento_id == $estabelecimento.id && $db.servicos.nome == "Atendimento Geral"
      return = {type: "single"}
    } as $servico_geral
  
    db.query filas {
      where = $db.filas.servico_id == $servico_geral.id && $db.filas.nome == "Atendimento Geral"
      return = {type: "single"}
    } as $fila_geral_existente
  
    conditional {
      if ($fila_geral_existente == null) {
        db.add filas {
          data = {
            servico_id: $servico_geral.id
            nome      : "Atendimento Geral"
            status    : "aberta"
          }
        } as $nova_fila_geral
      }
    }
  
    db.query servicos {
      where = $db.servicos.estabelecimento_id == $estabelecimento.id && $db.servicos.nome == "Preferencial"
      return = {type: "single"}
    } as $servico_preferencial_existente
  
    conditional {
      if ($servico_preferencial_existente == null) {
        db.add servicos {
          data = {
            estabelecimento_id: $estabelecimento.id
            nome              : "Preferencial"
            tempo_estimado    : 10
          }
        } as $novo_servico_preferencial
      }
    }
  
    db.query servicos {
      where = $db.servicos.estabelecimento_id == $estabelecimento.id && $db.servicos.nome == "Preferencial"
      return = {type: "single"}
    } as $servico_preferencial
  
    db.query filas {
      where = $db.filas.servico_id == $servico_preferencial.id && $db.filas.nome == "Preferencial"
      return = {type: "single"}
    } as $fila_preferencial_existente
  
    conditional {
      if ($fila_preferencial_existente == null) {
        db.add filas {
          data = {
            servico_id: $servico_preferencial.id
            nome      : "Preferencial"
            status    : "aberta"
          }
        } as $nova_fila_preferencial
      }
    }
  
    security.create_uuid as $totem_password
    db.query usuarios {
      where = $db.usuarios.email == "totem@filasmart.com"
      return = {type: "single"}
    } as $totem_existente
  
    conditional {
      if ($totem_existente == null) {
        db.add usuarios {
          data = {
            name    : "Totem Matriz"
            email   : "totem@filasmart.com"
            password: $totem_password
            role    : "totem"
          }
        } as $novo_totem
      }
    }
  
    db.query usuarios {
      where = $db.usuarios.email == "totem@filasmart.com"
      return = {type: "single"}
    } as $totem
  
    precondition ($totem.role == "totem") {
      error_type = "inputerror"
      error = "A conta totem@filasmart.com já existe fora do fixture esperado."
    }
  
    security.create_uuid as $tv_credential
    db.query tv_displays {
      where = $db.tv_displays.estabelecimento_id == $estabelecimento.id && $db.tv_displays.ativo == true
      return = {type: "single"}
    } as $display_existente
  
    conditional {
      if ($display_existente == null) {
        db.add tv_displays {
          data = {
            estabelecimento_id: $estabelecimento.id
            credential_hash   : $tv_credential|sha256
            ativo             : true
          }
        } as $novo_display
      }
    }
  }

  response = {
    success              : true
    estabelecimento      : $estabelecimento.nome
    usuarios             : ["admin@filasmart.com", "atendente1@filasmart.com", "atendente2@filasmart.com", "totem@filasmart.com"]
    filas                : ["Atendimento Geral", "Preferencial"]
    credenciais_unica_vez: ```
      {
        atendente1_password: ($atendente1_existente == null) ? $atendente1_password : null
        atendente2_password: ($atendente2_existente == null) ? $atendente2_password : null
        totem_password: ($totem_existente == null) ? $totem_password : null
        tv_display: ($display_existente == null) ? $tv_credential : null
      }
      ```
  }
}