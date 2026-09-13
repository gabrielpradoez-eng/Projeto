// Add PAPEL record
query papel verb=POST {
  api_group = "CRUD_APIS_BASICO"

  input {
    dblink {
      table = "PAPEL"
    }
  }

  stack {
    db.add PAPEL {
      enforce_hidden_fields = false
      data = {created_at: "now", papel: $input.papel}
    } as $model
  }

  response = $model
  guid = "XBq_eUDq9nc2OyNVUyMpr7bpHXU"
}