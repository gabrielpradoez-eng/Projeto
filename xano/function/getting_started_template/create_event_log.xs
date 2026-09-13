// Creates a record in the event log table
// 
function "Getting Started Template/create_event_log" {
  input {
    email to_email? filters=trim|lower
    text subject? filters=trim
    text body? filters=trim
  }

  stack {
    // Add a new user event log entry
    db.add "" {
      enforce_hidden_fields = false
      data = {
        created_at: "now"
        user_id   : $input.user_id
        account_id: $input.account_id
        action    : $input.action
        metadata  : $input.metadata
      }
    } as $new_log_entry
  }

  response = null
  tags = ["xano:quick-start"]
  guid = "qn6tsHnk4r38shx6w7fsOrQ2R_8"
}