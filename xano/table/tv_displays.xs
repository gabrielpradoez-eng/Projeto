// Credenciais de leitura pública, restritas por estabelecimento
table tv_displays {
  auth = false

  schema {
    int id
    timestamp created_at?=now
    int estabelecimento_id {
      table = "estabelecimentos"
    }
    text credential_hash
    bool ativo?=true
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "credential_hash"}]}
    {type: "btree", field: [{name: "estabelecimento_id"}]}
  ]
}