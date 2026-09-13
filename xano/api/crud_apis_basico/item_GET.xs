// Query all ITEM records
query item verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
  }

  stack {
    db.query ITEM {
      return = {type: "list"}
    } as $model
  }

  response = $model
  guid = "afej1wjmoj8DASYjfBYolp4ROi8"
}