// Produtos cadastrados que
// podem ser incluídos como Itens de Pedidos
// dos Cliente
table PRODUTO {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    text nome? filters=trim
    text descricao? filters=trim
    int qtd_disp?
    text url_imagem? filters=trim
    decimal preco?
    bool precisa_produzir?
    text categoria?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree|unique", field: [{name: "nome", op: "asc"}]}
  ]

  guid = "K2TP8vzchZi_kXjG7EysW49r6gY"
}