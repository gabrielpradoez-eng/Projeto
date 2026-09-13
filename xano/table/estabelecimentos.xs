// Cadastro dos locais físicos onde os serviços são prestados
table estabelecimentos {
  auth = false

  schema {
    int id
    timestamp created_at?=now
    text nome
    text endereco?
  }

  index = [{type: "primary", field: [{name: "id"}]}]
  guid = "daH0TTnnmlqf9LRb_x-WQrnyRgg"
}