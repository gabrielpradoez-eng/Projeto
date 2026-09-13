// Get PAPEL record
query "papel/{papel_id}" verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
    int papel_id? filters=min:1
  }

  stack {
    db.get PAPEL {
      field_name = "id"
      field_value = $input.papel_id
    } as $model
  
    precondition ($model != null) {
      error_type = "notfound"
      error = "Not Found"
    }
  }

  response = $model
  guid = "3ydT_4FR2Va7kukzildrBB74p04"
}