// Get FAQ record
query "faq/{faq_id}" verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
    int faq_id? filters=min:1
  }

  stack {
    db.get FAQ {
      field_name = "id"
      field_value = $input.faq_id
    } as $model
  
    precondition ($model != null) {
      error_type = "notfound"
      error = "Not Found"
    }
  }

  response = $model
  guid = "6H-wPOEjlWuFY0-TMAOTdFmcrek"
}