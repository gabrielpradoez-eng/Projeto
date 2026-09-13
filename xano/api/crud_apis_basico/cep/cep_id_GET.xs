// Get CEP record
query "cep/{cep_id}" verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
    int cep_id? filters=min:1
  }

  stack {
    db.get CEP {
      field_name = "id"
      field_value = $input.cep_id
    } as $model
  
    precondition ($model != null) {
      error_type = "notfound"
      error = "Not Found"
    }
  }

  response = $model
  guid = "KJDvi5A60WB8dA8dldwPpOkYq7A"
}