// Query all PAPEL records
query papel verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
  }

  stack {
    db.query PAPEL {
      return = {type: "list"}
    } as $model
  }

  response = $model
  guid = "BcPrpslWTvBc8s-yHSuu-hSYqXY"
}