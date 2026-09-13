// Update FAQ record
query "faq/{faq_id}" verb=PUT {
  api_group = "CRUD_APIS_BASICO"

  input {
    int faq_id? filters=min:1
    dblink {
      table = "FAQ"
    }
  }

  stack {
    db.edit FAQ {
      field_name = "id"
      field_value = $input.faq_id
      enforce_hidden_fields = false
      data = {pergunta: $input.pergunta, resposta: $input.resposta}
    } as $model
  }

  response = $model
  guid = "3h2nZ9WHmgNOONgGgvq1FFbvFIk"
}