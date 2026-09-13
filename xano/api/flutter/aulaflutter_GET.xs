// Query all aulaflutter records
query aulaflutter verb=GET {
  api_group = "flutter"

  input {
  }

  stack {
    db.query aulaflutter {
      return = {type: "list"}
    } as $aulaflutter
  }

  response = $aulaflutter
  guid = "aPZ_pmIRn9_rFf2VhJiRoCMJdGs"
}