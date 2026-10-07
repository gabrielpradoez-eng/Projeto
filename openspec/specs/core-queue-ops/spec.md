# Core Queue Operations Specification

## Purpose
Define the baseline operational capabilities of the FilaSmart core: authentication, user roles, establishment and service setup, queue lifecycle, ticket issuance, attendant calling flow, and service completion with auditing.

## Requirements

### Requirement: Authentication and role-based access
The system SHALL authenticate users with valid credentials and restrict protected actions according to role and establishment ownership.

#### Scenario: Successful login
- **WHEN** a registered user submits valid credentials
- **THEN** the system SHALL return an authenticated session containing the user identity and role.

#### Scenario: Unauthorized operation
- **WHEN** a user attempts an action outside their permissions
- **THEN** the system SHALL reject the request and record the action in the audit log.

### Requirement: Establishment and service setup
The system SHALL support the registration of establishments and the definition of services tied to those establishments.

#### Scenario: Register service
- **WHEN** an administrator creates a service for an establishment
- **THEN** the service SHALL be linked to that establishment and store the estimated handling time.

### Requirement: Queue lifecycle and ticket issuance
The system SHALL support open and closed queues and generate sequential ticket numbers within each queue.

#### Scenario: Ticket emission
- **WHEN** a valid user requests a ticket in an open queue
- **THEN** the system SHALL assign the next available number and persist the ticket in waiting status.

### Requirement: Queue calling and attendance workflow
The system SHALL allow an active attendant to call the next available ticket and register the start of an attendance cycle.

#### Scenario: Call next ticket
- **WHEN** an active attendant triggers the next call in the queue for their establishment
- **THEN** the system SHALL select the lowest waiting ticket, set it to called, and create an attendance record.

### Requirement: Service completion and auditability
The system SHALL complete the attendance lifecycle and persist operational events for traceability.

#### Scenario: Finish service
- **WHEN** the called ticket is completed
- **THEN** the system SHALL close the attendance, set the ticket status to completed, and log the event.

### Requirement: Queue operations baseline
The system SHALL preserve the existing queue behavior while introducing role validation, establishment isolation, and auditing as part of the delivery baseline.

#### Scenario: Baseline conservation
- **WHEN** the queue core is executed in production-like conditions
- **THEN** the system SHALL maintain consistent ordering, access control, and lifecycle status management without relying on frontend-only rules.

### Requirement: Establishment isolation
The system SHALL ensure that attendants and their operations remain isolated to the proper establishment and queue scope.

#### Scenario: Cross-establishment access attempt
- **WHEN** an attendant attempts to operate on a queue outside their establishment
- **THEN** the system SHALL deny access and leave the queue unchanged.
