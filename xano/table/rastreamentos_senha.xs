// Autorizações temporárias para consulta individual de uma senha
table rastreamentos_senha {
  auth = false

  schema {
    int id
    timestamp created_at?=now
    int senha_id {
      table = "senhas"
    }
    text referencia_hash
    timestamp expira_at
    timestamp revogada_at?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "referencia_hash"}]}
    {type: "btree", field: [{name: "senha_id"}]}
    {type: "btree", field: [{name: "expira_at"}]}
  ]
  guid = "R8yYpB1isoCTDATQeQOwxVQsM9M"
}