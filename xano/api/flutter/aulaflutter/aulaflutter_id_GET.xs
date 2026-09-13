// Get aulaflutter record
query "aulaflutter/{aulaflutter_id}" verb=GET {
  api_group = "flutter"

  input {
    int aulaflutter_id? filters=min:1
  }

  stack {
    db.get aulaflutter {
      field_name = "id"
      field_value = $input.aulaflutter_id
    } as $aulaflutter
  
    precondition ($aulaflutter != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $aulaflutter
  guid = "gw1oLNnybwf3pmgnLjVdauoPA4I"
}