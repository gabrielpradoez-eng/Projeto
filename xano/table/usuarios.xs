// Tabela central de usuários e autenticação
table usuarios {
  auth = true

  schema {
    int id
    timestamp created_at?=now
    text name
    email email
    password password
    enum role?=usuario {
      values = ["admin", "atendente", "usuario", "totem"]
    }

    int estabelecimento_id? {
      table = "estabelecimentos"
    }

    json password_reset?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "email"}]}
  ]

  guid = "pIGW_wfK7gWjFjPmx7iAfZyKgnM"
}