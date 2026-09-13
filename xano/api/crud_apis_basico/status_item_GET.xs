// Query all STATUS_ITEM records
query status_item verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
  }

  stack {
    db.query STATUS_ITEM {
      return = {type: "list"}
    } as $model
  }

  response = $model
  guid = "k1mCY6Hcf1khXyBbgW4HUGomyFo"
}