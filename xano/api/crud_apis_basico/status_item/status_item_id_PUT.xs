// Update STATUS_ITEM record
query "status_item/{status_item_id}" verb=PUT {
  api_group = "CRUD_APIS_BASICO"

  input {
    int status_item_id? filters=min:1
    dblink {
      table = "STATUS_ITEM"
    }
  }

  stack {
    db.edit STATUS_ITEM {
      field_name = "id"
      field_value = $input.status_item_id
      enforce_hidden_fields = false
      data = {status: $input.status}
    } as $model
  }

  response = $model
  guid = "q5gbHDFYf3xFdttkUTP6NwaevCo"
}