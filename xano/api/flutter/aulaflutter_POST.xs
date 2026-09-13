// Add aulaflutter record
query aulaflutter verb=POST {
  api_group = "flutter"

  input {
    dblink {
      table = "aulaflutter"
    }
  }

  stack {
    db.add aulaflutter {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $aulaflutter
  }

  response = $aulaflutter
  guid = "pCdjGPzY5CvGTcpraEdbwhRAT2E"
}