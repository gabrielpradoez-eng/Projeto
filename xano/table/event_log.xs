// Tabela de log de auditoria
table event_log {
  auth = false

  schema {
    int id
    timestamp created_at?=now
    int user_id {
      table = "usuarios"
    }
  
    text action
    json metadata?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "user_id"}]}
    {type: "btree", field: [{name: "action"}]}
  ]

  guid = "lcUrvyPUvo6Yfnk_VmjHHnB83cQ"
}