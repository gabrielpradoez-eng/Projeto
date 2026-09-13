// Edit STATUS_ITEM record
query "status_item/{status_item_id}" verb=PATCH {
  api_group = "CRUD_APIS_BASICO"

  input {
    int status_item_id? filters=min:1
    dblink {
      table = "STATUS_ITEM"
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch STATUS_ITEM {
      field_name = "id"
      field_value = $input.status_item_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $model
  }

  response = $model
  guid = "0xc_NqPe1qFgPRDtTx4u602bEx0"
}