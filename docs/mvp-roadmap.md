# MVP Roadmap (MCQ-first)

Target date for first usable MCQ-only MVP: 2026-05-29

## Phase 0 - Setup and Contracts (Week 1)

1. Create monorepo structure and CI baseline.
2. Define schema files and contract docs (MCQ first, shared core second).
3. Add migration scaffold for schema version 1.0.
4. Add dependency license guardrails in CI.

Exit criteria:
1. Schema contracts compile/validate.
2. CI checks pass on baseline repository.

## Phase 1 - Core Validation and Packaging (Week 1-2)

1. Implement Rust validator with error/warning taxonomy.
2. Implement deterministic ZIP builder in Rust.
3. Enforce LF normalization, fixed file order, fixed metadata timestamps, Deflate level 6.
4. Implement security checks (path traversal, absolute paths, symlink blocking).

Exit criteria:
1. MCQ sample package validates correctly.
2. Invalid samples fail with actionable errors.
3. Determinism test passes across repeated runs.

## Phase 2 - Ingestion and LLM Draft (Week 2-3)

1. Implement Python ingestion for PDF, DOCX, MD, TXT.
2. Add scanned PDF detection and OCR fallback warning/manual mode.
3. Add Ollama adapter for draft generation.
4. Persist full audit trail data to project.json.

Exit criteria:
1. Imported source can be converted to draft schema.
2. Prompt/response and model metadata are captured.

## Phase 3 - Desktop Workflow (Week 3-4)

1. Build Tauri + frontend workflow:
   - project create/open
   - multi-problem navigation
   - import and draft
   - review/edit
   - validation panel
   - approval gate
   - export
2. Add warning confirmation modal and typed acknowledgment for high-risk warnings.
3. Add org policy settings and project snapshot embed.

Exit criteria:
1. User can create and export a validated MCQ package end-to-end.
2. Exported artifacts include all required files.

## Phase 4 - Hardening and Release (Week 4-5)

1. Add test coverage for validator and packager to >= 85%.
2. Add integration tests for multi-problem bulk export.
3. Add audit log retention cleanup logic (default 180 days).
4. Build Windows installer and run smoke tests on Win10 22H2 and Win11.

Exit criteria:
1. MCQ-only MVP usable by internal pilot users.
2. Release candidate installer is generated.

## Non-MVP Deferred Items

1. Server-import preflight.
2. Full OCR pipeline.
3. Auto-update.
4. Full wrapper execution validation.
5. Programming workflow completion (starts immediately after MCQ MVP baseline).

## Immediate Execution Backlog

1. Scaffold monorepo directories and base build tooling.
2. Implement MCQ manifest schema and validator rules.
3. Implement deterministic zip packager with reproducibility tests.
4. Wire minimal UI flow for import -> validate -> approve -> export.
5. Add artifact generation and audit snapshots in project.json.
