# Spec Delta

## Purpose

Даёт текстовый CLI к Notify Mini, чтобы пользователь мог вызывать subscribe/list/unsubscribe без импорта модуля вручную.

## ADDED Requirements

### Requirement: CLI exposes core commands
The CLI SHALL support commands `subscribe <name>`, `list`, `unsubscribe <name>`, and `help`, and MUST exit with code 0 on success.

#### Scenario: Subscribe via CLI
- **WHEN** the user runs `python cli.py subscribe Ann`
- **THEN** the process exits 0 and prints a short success line containing `Ann`

#### Scenario: List via CLI
- **WHEN** subscribers exist and the user runs `python cli.py list`
- **THEN** the process exits 0 and prints one name per line in sorted order

#### Scenario: Help via CLI
- **WHEN** the user runs `python cli.py help` or `python cli.py` without args
- **THEN** the process exits 0 and prints available commands

### Requirement: CLI maps domain errors to non-zero exit
On domain errors from the service (`empty name`, `unknown name`) the CLI SHALL print the error text to stderr and exit with code 1. On unknown command the CLI SHALL exit with code 2.

#### Scenario: Unsubscribe unknown name
- **WHEN** the user runs `python cli.py unsubscribe Ghost` and that name is not subscribed
- **THEN** the process exits 1 and stderr contains `unknown name`

#### Scenario: Unknown command
- **WHEN** the user runs `python cli.py bounce Ann`
- **THEN** the process exits 2 and stderr explains that the command is unknown
