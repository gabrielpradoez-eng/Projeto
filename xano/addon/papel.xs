addon _papel {
  input {
    int PAPEL_id? {
      table = "PAPEL"
    }
  }

  stack {
    db.query PAPEL {
      where = $db.PAPEL.id == $input.PAPEL_id
      return = {type: "single"}
    }
  }

  guid = "oFxC6WleliwqBhzDM8nRqvJ8znE"
}