// Add CARTAOTOKNZD record
query cartaotoknzd verb=POST {
  api_group = "CRUD_APIS_BASICO"

  input {
    dblink {
      table = "CARTAOTOKNZD"
    }
  }

  stack {
    db.add CARTAOTOKNZD {
      enforce_hidden_fields = false
      data = {
        created_at        : "now"
        cliente_id        : $input.cliente_id
        token             : $input.token
        codigoclienteassas: $input.codigoclienteassas
      }
    } as $model
  }

  response = $model
  guid = "3nWsfW05c88uR3NpviT7CoCig0Q"
}