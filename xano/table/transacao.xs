// Log ou registro de transações
// envolvendo pagamentos com cartões de
// crédito
table TRANSACAO {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    text clienteassas? filters=trim
    text idpayment? filters=trim
    text tipo? filters=trim
    int valor?
    text datavenc? filters=trim
    text descricao? filters=trim
    int statustransacao_id?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]

  guid = "MA9neql2CHbisQ11yJjH441XPJk"
}