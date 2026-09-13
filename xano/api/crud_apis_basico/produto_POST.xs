// Add PRODUTO record
query produto verb=POST {
  api_group = "CRUD_APIS_BASICO"

  input {
    dblink {
      table = "PRODUTO"
    }
  }

  stack {
    db.add PRODUTO {
      enforce_hidden_fields = false
      data = {
        created_at      : "now"
        nome            : $input.nome
        descricao       : $input.descricao
        qtd_disp        : $input.qtd_disp
        url_imagem      : $input.url_imagem
        preco           : $input.preco
        precisa_produzir: $input.precisa_produzir
      }
    } as $model
  }

  response = $model
  guid = "mAJ07M9LlxUVJLEcqyFUPTLjCGk"
}