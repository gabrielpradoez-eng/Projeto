// Query all OE records
query oe verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
  }

  stack {
    db.query OE {
      return = {type: "list"}
    } as $model
  }

  response = $model
  guid = "rTz7Zn3mYkHRRgsg7xgAphHJygk"
}