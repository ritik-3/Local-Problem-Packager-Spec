# Local Problem Packager - Architecture Freeze (MVP)

Date: 2026-04-25
Target MVP (MCQ-first): 2026-05-29

## 1. Scope Freeze

1. MVP v1 focuses on MCQ packaging first.
2. Programming packaging follows immediately after MCQ baseline is stable.
3. Desktop app stack is Tauri (Windows-only for MVP).
4. Core backend is Rust + Python hybrid.

## 2. Platform and Runtime Decisions

1. Desktop framework: Tauri.
2. Core language split:
   - Rust: packaging engine, path safety, deterministic ZIP generation, core validation.
   - Python sidecar: PDF/DOCX/MD/TXT ingestion, optional OCR bridge, LLM orchestration.
3. LLM runtime: Ollama first.
4. Default recommended model families:
   - qwen2.5-instruct 7B or 14B (hardware-dependent recommendation only).
   - fallback: llama3.1 8B instruct.
5. Model switching: manual in settings for MVP.

## 3. Offline and Security Policy

1. Offline-first and offline-by-default.
2. Outbound network is disabled unless explicitly enabled in settings.
3. Symlinks are always blocked (including source folders).
4. Path traversal and absolute path references are blocked.
5. Minimum OS target:
   - Windows 10 22H2
   - Windows 11

## 4. Import and Extraction Policy

1. Supported input formats in MVP:
   - PDF
   - DOCX
   - Markdown
   - TXT
2. OCR strategy in MVP:
   - no full OCR feature set
   - if scanned PDF is detected and OCR dependency is missing, continue with warning and switch to manual text mode

## 5. Canonical Package Contracts

## 5.1 MCQ Contract (MVP primary)

1. Current sample layout is provisional but accepted as MVP baseline.
2. Canonical metadata filename for MCQ: manifest.json.
3. MCQ package layout uses deterministic folder naming and stable references.

## 5.2 Programming Contract (MVP secondary)

1. Supported languages:
   - python
   - cpp
   - java
   - c
2. Language whitelist is configurable per organization via settings.

## 5.3 Shared Contract Rules

1. `schema_version` starts at 1.0.
2. Minimal migration scaffold must exist in MVP (1.0 -> 1.0 no-op supported).
3. Stub/wrapper references support both inline and file path values.
4. UI should prefer file paths and warn for long inline values.

## 6. Validation Policy

1. Errors block export.
2. Warnings do not block export, but require explicit per-export confirmation.
3. High-risk warnings require typed acknowledgment.
4. Wrapper validation in MVP is schema/path-based only.
5. Optional syntax sanity checks are allowed if low-friction.
6. Test case limits:
   - default max: 50 per language
   - configurable per organization
   - hard cap: 200 per language

## 7. Deterministic Build Policy

1. Deterministic output target: byte-for-byte stable ZIP across machines.
2. Required determinism controls:
   - fixed file ordering
   - LF line endings for exported text artifacts
   - fixed ZIP metadata timestamps
   - Deflate compression level 6 for all files

## 8. Uniqueness Rules

1. Slug and code must be unique within current project and current export package (blocking).
2. Optional local registry uniqueness check is warning-only in MVP.

## 9. Artifacts and Audit

1. Required export artifacts:
   - package.zip
   - project.json
   - validation-report.json
   - checksum.sha256
2. Checksum algorithm: SHA-256.
3. project.json must include:
   - raw extracted text snapshots
   - full LLM prompts and responses
   - model and version metadata
   - timestamps
4. Organization policy source:
   - machine-level local settings file (authoritative)
   - read-only policy snapshot written into project.json for audit traceability

## 10. UX and Workflow Policy

1. MVP supports multi-problem projects.
2. Human approval checkbox is mandatory before export.
3. Server import preflight is phase 2 (not MVP).
4. MVP preflight mirrors local validator only.

## 11. Logging and Retention

1. Audit logs are stored locally in app data directory.
2. Logs are both project-scoped and globally summarized.
3. Retention default is 180 days and configurable.

## 12. Repository and Quality Policy

1. Monorepo from day one with clear module boundaries.
2. Coverage targets:
   - validator and packager modules >= 85%
   - overall project initial target around 70%
3. UI priority: functional and clear MVP over design-heavy polish.

## 13. License Policy

1. Block GPL and AGPL runtime dependencies.
2. Allow MIT, Apache-2.0, and BSD licenses.

## 14. Release Policy

1. Manual installer only in MVP.
2. Auto-update deferred to phase 2 after signing and release pipeline stabilization.
