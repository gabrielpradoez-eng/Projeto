// Query all STATUS_OE records
query status_oe verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
  }

  stack {
    db.query STATUS_OE {
      return = {type: "list"}
    } as $model
  }

  response = $model
  guid = "-3D1Avti_uKk1MdjeSSjkONy-SQ"
}