query upsertCEP verb=POST {
  api_group = "APIs Customizadas"

  input {
    text cep? filters=trim
    text cidade? filters=trim
    text estado? filters=trim
  }

  stack {
    db.query CEP {
      where = $db.CEP.cep == $input.cep
      return = {type: "list"}
    } as $CEP1
  
    conditional {
      if ($var.CEP1[0].cep == $input.cep) {
        db.patch CEP {
          field_name = "id"
          field_value = $var.CEP1[0].id
          data = {uf: $input.cidade, estado: $input.estado}
        } as $CEP2
      }
    
      else {
        db.add CEP {
          enforce_hidden_fields = false
          data = {
            created_at: "now"
            cep       : $input.cep
            uf        : $input.estado
            cidade    : $input.cidade
          }
        } as $CEP2
      }
    }
  }

  response = $CEP2
  guid = "sZdYWscxxERHixLP-wTj3OXGtnA"
}