# MCQ Problem Builder - End-to-End Implementation Guide

Date: 2026-04-25  
Scope: MCQ-first MVP for Local Problem Packager  
Target MVP date: 2026-05-29

## 1. Purpose

This guide is the execution manual for building the MCQ builder end-to-end.
It translates product and architecture decisions into implementation steps, module boundaries, APIs, tests, and release gates.

Use this guide as the source of truth for engineering execution.

## 2. Frozen Decisions (Operationalized)

1. Desktop app stack: Tauri + React + TypeScript.
2. Backend architecture: Rust core + Python sidecar.
3. Local model runtime: Ollama (manual model selection in MVP).
4. Supported imports in MVP: PDF, DOCX, Markdown, TXT.
5. OCR in MVP: no full OCR; warn and switch to manual mode when scanned PDF is detected and OCR dependency is missing.
6. Offline mode: enabled by default; no outbound network unless explicitly enabled.
7. MCQ metadata canonical filename: manifest.json.
8. Validation behavior: errors block export; warnings require confirmation; high-risk warnings require typed acknowledgment.
9. Deterministic build target: byte-identical ZIP across machines.
10. Deterministic controls: fixed file order, LF line endings, fixed ZIP timestamps, Deflate level 6.
11. Security requirements: block symlinks, path traversal, absolute paths.
12. Required artifacts: package.zip, project.json, validation-report.json, checksum.sha256.
13. Checksum algorithm: SHA-256.
14. Logging: project-scoped + global logs, default retention 180 days.
15. License policy: block GPL/AGPL runtime dependencies; allow MIT/Apache-2.0/BSD.
16. Windows MVP target: Windows 10 22H2 and Windows 11.

## 3. End-to-End Product Flow (MCQ)

1. Create or open a multi-problem project.
2. Import one or more source files per MCQ (PDF/DOCX/MD/TXT).
3. Extract text and layout hints through Python sidecar.
4. Generate draft MCQ schema with local LLM (Ollama) or manual mode.
5. Review and edit all fields in UI.
6. Run validator and show errors/warnings.
7. Require human approval checkbox.
8. For high-risk warnings, require typed acknowledgment.
9. Build canonical staging structure.
10. Generate deterministic ZIP.
11. Generate project.json, validation-report.json, checksum.sha256.
12. Write audit logs.

## 4. Canonical MCQ Packaging Contract (MVP)

## 4.1 Folder shape inside package

```text
mcq/
  <problem-slug>/
    manifest.json
    question.md
    explanation.md
    options.csv
    tags.txt
    placement.yaml
```

Notes:
1. explanation.md is optional when policy permits, but missing explanation may emit warning.
2. All paths in manifest.json are relative to problem folder.

## 4.2 MCQ manifest.json (canonical v1.0)

```json
{
  "schema_version": "1.0",
  "problem_type": "mcq",
  "slug": "sample-general-math",
  "title": "Percentage Basics",
  "difficulty": "Easy",
  "question_file": "question.md",
  "explanation_file": "explanation.md",
  "options_file": "options.csv",
  "tags_file": "tags.txt",
  "placement_file": "placement.yaml",
  "category": "Aptitude",
  "subtopic": "Arithmetic",
  "practice_order": 5,
  "code": "MCQ-0001"
}
```

## 4.3 options.csv contract

Header:
```text
option_text,is_correct,feedback
```

Rules:
1. At least 2 options.
2. At least 1 correct option.
3. option_text non-empty.
4. is_correct accepted values: true/false (case-insensitive normalized to lowercase).
5. feedback optional.

## 4.4 tags.txt contract

Rules:
1. One tag per line.
2. Empty lines ignored.
3. Trim whitespace.
4. Deduplicate tags case-insensitively.

## 4.5 placement.yaml contract

Rules:
1. category required.
2. subtopic required.
3. order must be non-negative integer if present.

## 5. Project and Audit Contract

## 5.1 project.json minimum sections

```json
{
  "schema_version": "1.0",
  "project_id": "uuid-or-stable-id",
  "created_at": "2026-04-25T12:00:00Z",
  "updated_at": "2026-04-25T12:30:00Z",
  "org_policy_snapshot": {
    "language_whitelist": ["python", "cpp", "java", "c"],
    "max_testcases_per_language": 50,
    "hard_cap_testcases_per_language": 200
  },
  "problems": [
    {
      "problem_type": "mcq",
      "slug": "sample-general-math",
      "sources": [
        {
          "path": "input/problem.pdf",
          "sha256": "...",
          "imported_at": "2026-04-25T12:05:00Z"
        }
      ],
      "extraction": {
        "raw_text_snapshot": "...",
        "layout_hints": []
      },
      "llm": {
        "runtime": "ollama",
        "model": "qwen2.5-instruct:7b",
        "prompt": "...",
        "response": "...",
        "generated_at": "2026-04-25T12:10:00Z"
      }
    }
  ]
}
```

## 5.2 Policy precedence

1. Machine-level policy is authoritative.
2. project.json policy snapshot is read-only audit evidence.

## 6. Module Responsibilities

## 6.1 Rust crates

### core-schema

Responsibilities:
1. Schema version constants.
2. Shared Rust domain models (manifest, report, errors).
3. Migration interface (starting with 1.0 no-op).

### validator

Responsibilities:
1. Structural validation.
2. Semantic validation.
3. Security checks for paths and symlinks.
4. Severity classification: error, warning, high-risk warning.
5. Validation report generation.

### packager

Responsibilities:
1. Build canonical staging tree.
2. Normalize line endings to LF for exported text artifacts.
3. Deterministic ZIP creation (fixed order, fixed timestamp, level 6).
4. SHA-256 checksum generation.

## 6.2 Python sidecar (ingestion-py)

Responsibilities:
1. Parse PDF/DOCX/MD/TXT.
2. Detect scanned PDF and trigger OCR fallback warning/manual mode.
3. Build extraction output for UI and audit.
4. LLM orchestration via Ollama API calls.
5. Return structured draft payload to desktop app.

## 6.3 Desktop app (Tauri + React)

Responsibilities:
1. Project lifecycle screens.
2. Import and extraction workflows.
3. Draft and schema editor.
4. Validation panel and export gating.
5. Approval + high-risk typed acknowledgment flow.
6. Export orchestration and output directory management.
7. Settings page (offline toggle, model selection, org policy visibility).

## 7. Implementation Plan (Step-by-Step)

## Phase A - Contracts and Domain Model (2-3 days)

Tasks:
1. Finalize JSON schemas in schemas/mcq/v1.0 and schemas/shared/v1.0.
2. Define Rust structs and serde mappings.
3. Define validation error code taxonomy.
4. Define validation-report.json schema.

Definition of Done:
1. Schema validation tests pass.
2. All required fields mapped to structs.
3. Error code list is documented.

## Phase B - Validator Engine (4-5 days)

Tasks:
1. Implement manifest structural validation.
2. Implement file existence and relative-path checks.
3. Implement symlink/absolute/traversal blocking.
4. Implement options.csv validations.
5. Implement tags and placement validations.
6. Implement warning/high-risk classification.

Definition of Done:
1. sample_zip/MCQ_sample_zip validates with no blocking errors.
2. Invalid fixtures produce deterministic error codes/messages.
3. Unit coverage for validator crate reaches >= 85%.

## Phase C - Deterministic Packager (3-4 days)

Tasks:
1. Implement canonical staging folder writer.
2. Implement text normalization to LF.
3. Implement deterministic ZIP entry ordering.
4. Implement fixed ZIP timestamp and compression level 6.
5. Implement checksum.sha256 writer.

Definition of Done:
1. Same input produces byte-identical ZIP across repeated runs.
2. ZIP content and checksum are stable in CI.
3. packager crate coverage reaches >= 85%.

## Phase D - Ingestion and LLM Sidecar (4-5 days)

Tasks:
1. Implement format-specific extractors for PDF/DOCX/MD/TXT.
2. Implement scanned PDF detector.
3. Implement OCR dependency check and manual fallback signaling.
4. Implement Ollama adapter with timeout/error mapping.
5. Persist raw extraction, prompt/response, model metadata.

Definition of Done:
1. At least one sample from each input format can be imported.
2. Sidecar returns structured extraction payload.
3. Failure modes are surfaced with actionable messages.

## Phase E - Desktop Workflow (5-6 days)

Tasks:
1. Build project list and problem navigator.
2. Build import screen and extraction status.
3. Build MCQ form editor (manifest + files).
4. Build validator panel with severity filtering.
5. Build approval gate with typed acknowledgment for high-risk warnings.
6. Build export workflow and artifact status output.

Definition of Done:
1. User can do full MCQ flow without terminal commands.
2. Export produces all 4 required artifacts.
3. Validation gating behavior matches policy.

## Phase F - Hardening and Release (3-4 days)

Tasks:
1. Add integration tests for multi-problem export.
2. Add retention cleanup job on startup and after export.
3. Add dependency license policy check in CI.
4. Build Windows installer and smoke test.

Definition of Done:
1. CI green with coverage gates.
2. Installer generated and validated on target Windows versions.
3. Internal pilot sign-off received.

## 8. API Contracts (Recommended)

## 8.1 Tauri command interface (Rust)

1. validate_problem(problem_path_or_payload) -> validation report.
2. build_export(project_id, output_dir) -> artifact manifest.
3. compute_checksum(file_path) -> checksum string.
4. read_policy() -> machine policy snapshot.

## 8.2 Python sidecar interface

1. import_document(path) -> extracted text + metadata.
2. detect_scanned_pdf(path) -> bool + confidence + warning message.
3. generate_mcq_draft(extraction, model_config) -> draft manifest payload.

Transport options:
1. Start with stdio JSON-RPC or local HTTP loopback.
2. Keep request/response schemas versioned.

## 9. Validation Taxonomy

## 9.1 Blocking errors

Examples:
1. Missing manifest.json.
2. Invalid schema_version.
3. Unsafe path reference.
4. options.csv missing required columns.
5. No correct option present.

## 9.2 Standard warnings

Examples:
1. Missing explanation.md.
2. Very short statement text.
3. Low tag count.

## 9.3 High-risk warnings (typed acknowledgment)

Examples:
1. OCR fallback to manual mode.
2. Policy mismatch between project snapshot and machine policy.
3. Duplicate-similar slug detection.
4. Long inline content beyond threshold (500 lines or 64 KB).

## 10. Determinism Specification

1. ZIP timestamp for all entries: 1980-01-01T00:00:00Z.
2. Compression: Deflate level 6 for all files.
3. Entry order: lexical sort on normalized forward-slash paths.
4. Line endings: LF for exported text artifacts.
5. Stable serialization: deterministic JSON key order where feasible.

Determinism test pattern:
1. Export same project twice in clean temp folders.
2. Compare package.zip bytes.
3. Compare checksum.sha256 values.
4. Compare validation-report.json normalized content.

## 11. Security Implementation Checklist

1. Reject any absolute path in manifest references.
2. Reject any path containing parent traversal segments.
3. Resolve and verify all referenced files stay inside problem root.
4. Reject symlinks in source and staging trees.
5. Treat all imported content as untrusted.
6. Sanitize display rendering in UI (no unsafe HTML execution).

## 12. CI/CD Baseline

Jobs:
1. Rust: fmt + clippy + test + coverage.
2. Python: ruff + pytest.
3. Frontend: typecheck + build.
4. Schema checks: JSON schema validation.
5. License check: block GPL/AGPL runtime dependencies.
6. Determinism integration test.

Release pipeline (MVP):
1. Build signed or internal-trust installer manually.
2. Publish release notes and checksums.
3. Distribute installer for pilot usage.

## 13. Team Execution Plan (Role Split)

1. Rust owner: validator + packager + tauri command layer.
2. Python owner: ingestion + OCR fallback + Ollama adapter.
3. Frontend owner: project flow + editor + validation UX + export UX.
4. QA owner: fixtures + integration + determinism + security test matrix.

## 14. Week-by-Week Plan to Target Date

Week 1:
1. Contracts done.
2. Validator base implemented.
3. Initial fixture tests.

Week 2:
1. Deterministic packager complete.
2. Checksums and reports complete.
3. CI determinism checks active.

Week 3:
1. Ingestion sidecar complete for all formats.
2. Ollama draft generation connected.
3. project.json audit fields wired.

Week 4:
1. Full desktop workflow complete.
2. Validation and approval gating complete.
3. Multi-problem project flow stabilized.

Week 5 (buffer and release):
1. Hardening, regression fixes, release candidate.
2. Windows smoke tests.
3. Pilot handoff.

## 15. Acceptance Criteria (MVP Sign-Off)

1. End-to-end MCQ flow works for multi-problem project.
2. Export always creates all required artifacts.
3. Unsafe paths and symlinks are always blocked.
4. Warning and high-risk confirmation behavior is enforced.
5. Deterministic ZIP output is byte-identical across repeated runs.
6. Audit trail in project.json includes extraction snapshots and full LLM trace.
7. CI gates pass with target coverage thresholds.

## 16. Immediate Next Coding Tasks

1. Complete MCQ manifest schema fields and freeze error code list.
2. Implement validator rules and fixture-based tests.
3. Implement deterministic ZIP builder with timestamp/order/line-ending controls.
4. Implement first usable extraction pipeline for PDF/DOCX/MD/TXT.
5. Implement desktop import -> validate -> approve -> export happy-path.
