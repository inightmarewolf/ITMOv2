# subscriber-lifecycle Specification

## Purpose
Управляет жизненным циклом подписчика в памяти процесса: подписка уже есть, эта capability добавляет безопасную отписку по имени.

## Requirements

### Requirement: Unsubscribe removes an existing name
The system SHALL remove a subscribed name from the in-memory set when `unsubscribe(name)` is called with a known non-empty name after stripping whitespace.

#### Scenario: Successful unsubscribe
- **WHEN** `"Ann"` is already subscribed and the caller invokes `unsubscribe("Ann")`
- **THEN** the function returns `{"unsubscribed": True, "name": "Ann"}` and `"Ann"` is absent from `list_subscribers()`

#### Scenario: Name is trimmed like subscribe
- **WHEN** `"Ann"` is subscribed and the caller invokes `unsubscribe("  Ann  ")`
- **THEN** the system treats the name as `"Ann"` and removes that subscriber

### Requirement: Unsubscribe rejects empty input
The system SHALL reject empty or whitespace-only names with `ValueError("empty name")` and MUST NOT change the subscriber set.

#### Scenario: Empty name
- **WHEN** the caller invokes `unsubscribe("   ")`
- **THEN** a `ValueError("empty name")` is raised and the subscriber set is unchanged

### Requirement: Unsubscribe rejects unknown name
The system SHALL raise `ValueError("unknown name")` when the trimmed name is not currently subscribed, and MUST NOT change other subscribers.

#### Scenario: Unknown name
- **WHEN** only `"Bob"` is subscribed and the caller invokes `unsubscribe("Ann")`
- **THEN** a `ValueError("unknown name")` is raised and `"Bob"` remains subscribed
