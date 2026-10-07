## MODIFIED Requirements

### Requirement: Queue calling and attendance workflow
The system SHALL allow an active attendant to call the next available ticket, register the start of an attendance cycle, and publish the resulting canonical call state for authorized public displays.

#### Scenario: Call next ticket
- **WHEN** an active attendant triggers the next call in the queue for their establishment
- **THEN** the system SHALL select the lowest waiting ticket, set it to called, create an attendance record, and make the resulting call and destination available to the authorized display feed.

#### Scenario: Public display reads canonical call state
- **WHEN** an authorized display requests the current call and recent call history
- **THEN** the system SHALL return the canonical current state and backend-ordered history for that display's authorized scope, and clients SHALL NOT independently select, reorder, or infer calls.

#### Scenario: No waiting ticket
- **WHEN** an active attendant requests the next call and no ticket is waiting
- **THEN** the system SHALL report that no call can be made and SHALL leave the current call state unchanged.