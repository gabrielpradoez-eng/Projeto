// Query all pratos records
query produto_bebida verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
  }

  stack {
    db.query PRODUTO {
      where = $db.PRODUTO.categoria == "sucos"
      return = {type: "list"}
    } as $model
  }

  response = $model
  guid = "EZw5DOdv5S01ttKtl-1UQj60hwQ"
}