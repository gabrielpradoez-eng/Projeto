// Add FAQ record
query faq verb=POST {
  api_group = "CRUD_APIS_BASICO"

  input {
    dblink {
      table = "FAQ"
    }
  }

  stack {
    db.add FAQ {
      enforce_hidden_fields = false
      data = {
        created_at: "now"
        pergunta  : $input.pergunta
        resposta  : $input.resposta
      }
    } as $model
  }

  response = $model
  guid = "jxtE7vbjGjo6Tx8POnnoMER8QoU"
}