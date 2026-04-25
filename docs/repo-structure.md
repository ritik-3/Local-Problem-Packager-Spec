# Repository Structure

## Apps

- `apps/desktop`: React frontend with Tauri host.

## Rust crates

- `crates/core-schema`: shared schema models and version constants.
- `crates/validator`: validation rules and severity taxonomy.
- `crates/packager`: deterministic ZIP assembly and checksum logic.

## Python services

- `services/ingestion-py`: source ingestion and LLM orchestration sidecar.

## Schemas

- `schemas/mcq/v1.0`: MCQ manifest schema.
- `schemas/shared/v1.0`: shared project schema.

## Tests and fixtures

- `samples/golden`: valid fixture packages.
- `samples/invalid`: invalid fixture packages.
- `tests/integration`: cross-module integration tests.
