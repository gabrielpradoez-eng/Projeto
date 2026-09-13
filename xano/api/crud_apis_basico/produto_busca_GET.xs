// Query all PRODUTO records
query produto_Busca verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
    text input? filters=trim
  }

  stack {
    db.query PRODUTO {
      where = ($db.PRODUTO.nome|to_lower) includes ($input.input|to_lower)
      return = {type: "list"}
    } as $model
  }

  response = $model
  guid = "koiNNKuYS060DlP8GS7QfaiB4wE"
}