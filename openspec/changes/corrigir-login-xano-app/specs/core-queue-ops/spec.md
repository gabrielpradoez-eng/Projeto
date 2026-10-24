## MODIFIED Requirements

### Requirement: Authentication and role-based access
The system SHALL authenticate users with valid credentials and restrict protected actions according to role and establishment ownership. A successful login SHALL establish the application session from the identity and role returned by the authentication backend, without inferring a local identity or privilege.

#### Scenario: Successful login
- **WHEN** a registered user submits valid credentials and the backend returns an authentication token and valid user identity
- **THEN** the system SHALL return an authenticated session containing the backend identity, role, and establishment scope when provided.

#### Scenario: Backend role values are recognized
- **WHEN** the backend returns a supported FilaSmart role (`admin`, `atendente`, or `usuario`)
- **THEN** the application SHALL preserve its authorization meaning for that role and SHALL NOT treat `atendente` or `usuario` as an unknown or administrative role.

#### Scenario: Malformed authentication response
- **WHEN** the backend response omits a valid authentication token, user identity, or supported role
- **THEN** the system SHALL reject login and SHALL NOT create a session from local sample data or assign a default privileged role.

#### Scenario: Unauthorized operation
- **WHEN** a user attempts an action outside their permissions
- **THEN** the system SHALL reject the request and record the action in the audit log.
