// Delete TOKENS record
query "tokens/{tokens_id}" verb=DELETE {
  api_group = "CRUD_APIS_BASICO"

  input {
    int tokens_id? filters=min:1
  }

  stack {
    db.del TOKENS {
      field_name = "id"
      field_value = $input.tokens_id
    }
  }

  response = null
  guid = "-i_I0aGAx-rDz84iV2Ng9vWeUp4"
}