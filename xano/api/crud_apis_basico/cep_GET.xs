// Query all CEP records
query cep verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
  }

  stack {
    db.query CEP {
      return = {type: "list"}
    } as $model
  }

  response = $model
  guid = "Km10Kg7ZF3PdDl20Q556iCJvyPM"
}