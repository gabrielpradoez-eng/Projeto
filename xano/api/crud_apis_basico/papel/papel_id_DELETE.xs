// Delete PAPEL record
query "papel/{papel_id}" verb=DELETE {
  api_group = "CRUD_APIS_BASICO"

  input {
    int papel_id? filters=min:1
  }

  stack {
    db.del PAPEL {
      field_name = "id"
      field_value = $input.papel_id
    }
  }

  response = null
  guid = "mmQRc3Q8rdr-s21EWEM0xLEZjLc"
}