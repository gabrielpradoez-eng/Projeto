query Colaborador_Sabor_Local verb=GET {
  api_group = "CRUD_APIS_BASICO"

  input {
  }

  stack {
    db.query USUARIO {
      where = $db.USUARIO.papel_id > 0
      return = {type: "list"}
      addon = [
        {
          name : "_papel"
          input: {PAPEL_id: $output.papel_id}
          as   : "__papel"
        }
        {
          name : "_papel"
          input: {PAPEL_id: $output.papel_id}
          as   : "__papel"
        }
      ]
    } as $USUARIO1
  }

  response = $USUARIO1
  guid = "gm8mu6-tCX3q5R01IDTZ1JHrTwc"
}