// Delete aulaflutter record.
query "aulaflutter/{aulaflutter_id}" verb=DELETE {
  api_group = "flutter"

  input {
    int aulaflutter_id? filters=min:1
  }

  stack {
    db.del aulaflutter {
      field_name = "id"
      field_value = $input.aulaflutter_id
    }
  }

  response = null
  guid = "bD6clmcqkXUG98djBNsAwzhy6h4"
}