// Delete OE record
query "oe/{oe_id}" verb=DELETE {
  api_group = "CRUD_APIS_BASICO"

  input {
    int oe_id? filters=min:1
  }

  stack {
    db.del OE {
      field_name = "id"
      field_value = $input.oe_id
    }
  }

  response = null
  guid = "88Fy9k-lbQZNGnEabbqMEhWooo0"
}