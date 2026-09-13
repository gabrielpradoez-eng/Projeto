// Query all sucos records
query produto_prato verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
  }

  stack {
    db.query PRODUTO {
      where = $db.PRODUTO.categoria == "pratos"
      return = {type: "list"}
    } as $model
  }

  response = $model
  guid = "jivf8PPTsBJDz90cnvvOobcg4VE"
}