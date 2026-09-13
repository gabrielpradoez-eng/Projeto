// Update STATUS_OE record
query "status_oe/{status_oe_id}" verb=PUT {
  api_group = "CRUD_APIS_BASICO"

  input {
    int status_oe_id? filters=min:1
    dblink {
      table = "STATUS_OE"
    }
  }

  stack {
    db.edit STATUS_OE {
      field_name = "id"
      field_value = $input.status_oe_id
      enforce_hidden_fields = false
      data = {status: $input.status}
    } as $model
  }

  response = $model
  guid = "2Inu4bPo_DY3_eQtcR8mho-glro"
}