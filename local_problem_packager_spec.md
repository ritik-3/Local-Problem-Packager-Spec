# Local Problem Packager Spec

## Purpose

This document defines the full product and technical specification for a local desktop application that converts source problem documents into a canonical bulk-upload ZIP package for the DDA Contest platform.

The tool exists to solve the current inconsistency problem caused by multiple authors generating ZIPs in different ways with different prompts, tools, and assumptions.

The intended operating model is:

1. A content creator provides a source document, usually PDF or DOCX.
2. The local app extracts the problem content.
3. A local LLM converts that content into a strict internal problem schema.
4. A human reviews and edits the structured data.
5. The app validates the package against one canonical spec.
6. The app builds one canonical ZIP.
7. The ZIP is optionally preflighted against the server-side importer contract.

The app must not generate arbitrary ZIP layouts. It must only generate the approved canonical format.

---

## 1. Executive Summary

### Business Problem

Problem authors currently source questions from PDFs, DOCX files, and mixed content repositories. They then use chatbots, ad hoc scripts, or personal tools to generate ZIP packages. This creates inconsistent manifests, missing testcase files, mismatched folder structures, vague metadata, and import failures.

### Proposed Solution

Build one local desktop application that acts as the only official problem-packaging tool. The app converts source documents into a strict structured schema, validates the result, and exports a canonical ZIP.

### Core Principle

The LLM assists content extraction and structuring. The application is responsible for correctness, validation, and final ZIP generation.

### Key Decision

The system should do both:

1. Standardize generation through a single tool.
2. Enforce strict validation so anything outside the spec is rejected.

This is the only sustainable approach.

---

## 2. Goals and Non-Goals

### Goals

- Eliminate ZIP inconsistency across authors.
- Support local-only operation on the creator's PC.
- Accept PDF and DOCX as the primary source inputs.
- Use a local LLM to extract and normalize content.
- Produce a single canonical ZIP format for programming problems.
- Support optional MCQ packaging if required later.
- Provide preview, validation, export, and auditability.
- Make package creation deterministic and repeatable.

### Non-Goals

- Do not allow arbitrary custom ZIP layouts.
- Do not let the LLM directly write final ZIP output without schema validation.
- Do not depend on cloud APIs for the core packaging workflow.
- Do not try to infer every possible author style or document format.
- Do not replace the server-side importer; the local app complements it.

---

## 3. Recommended Product Decision

The recommended solution is a local schema-driven packaging tool, not a free-form chatbot generator.

### Final Recommendation

Use a three-layer design:

1. Ingestion layer
   - Reads PDF/DOCX and extracts text/images/tables.
2. Structuring layer
   - Local LLM converts extracted content into a canonical problem schema.
3. Packaging layer
   - Validator and ZIP builder generate the final archive.

This architecture gives you consistency, privacy, and control.

### Why This Is Better Than Direct ZIP Generation

- The LLM is imperfect and will invent fields or miss constraints.
- A direct ZIP generator makes hidden errors hard to detect.
- A schema-based workflow makes review and debugging easier.
- The same schema can be reused by multiple creators and future tools.

---

## 4. Business Requirements Document (BRD)

### 4.1 Business Objective

Create one standardized packaging workflow so all problem authors produce the same shape of output regardless of source document, author skill, or tool choice.

### 4.2 Stakeholders

- Problem creators.
- Reviewer/approver team.
- Platform admins.
- Contest managers.
- Technical maintainers.

### 4.3 Business Pain Points

- Multiple sources of truth.
- Chatbot-generated ZIPs with inconsistent structure.
- Hidden missing files or malformed manifests.
- Rework by admins before import.
- Manual cleanup and troubleshooting.

### 4.4 Business Outcomes

- Reduced import failures.
- Reduced review time.
- Faster problem onboarding.
- Better quality control.
- Predictable ZIP output.

### 4.5 Success Metrics

- 95%+ of generated ZIPs import without manual repair.
- 0 accepted packages outside the canonical schema.
- Less than 5 minutes average authoring time for a standard problem after setup.
- Less than 10% of submissions require reviewer correction.

---

## 5. Functional Requirements Document (FRD)

### 5.1 Input Requirements

The app must accept at minimum:

- PDF files.
- DOCX files.
- Optional image attachments.
- Optional testcase input files.
- Optional source snippets pasted manually.

### Input Behavior

- The user can import one or more source files per problem.
- The app must retain the original source file references for audit purposes.
- The app must extract text and structural hints from the source files.
- The app must not silently discard source content.

### 5.2 Problem Types

The initial version should support:

- Programming problems.
- MCQ problems if you want a unified authoring workflow.

The recommended MVP focus is programming problems first.

### 5.3 Authoring Requirements

The app must allow the author to fill or confirm:

- Problem title.
- Slug.
- Difficulty.
- Description.
- Constraints.
- Function name.
- Function parameters.
- Return type.
- Supported languages.
- Starter code or stubs.
- Wrappers.
- Testcases.
- Tags.
- Category and subtopic for practice placement.
- Optional image and other assets.

### 5.4 Review Requirements

The app must show a preview before export:

- Rendered problem statement.
- Parsed metadata.
- Detected testcase count.
- Per-language testcase summaries.
- Stub/wrapper content preview.
- Validation warnings and errors.

The user must explicitly approve the final package before ZIP generation.

### 5.5 Export Requirements

The app must generate:

- A canonical ZIP package.
- A JSON/YAML project file for future edits.
- A validation report.
- Optional checksum/hash file.

### 5.6 Validation Requirements

The app must validate:

- ZIP folder structure.
- Manifest schema.
- Required fields.
- Language whitelist.
- Testcase JSON format.
- Referenced file existence.
- Maximum file sizes.
- Path traversal attempts.
- Duplicate or conflicting problem slugs.

### 5.7 Audit Requirements

The app must track:

- Source file names.
- Author identity if available.
- Timestamp.
- Model/version used.
- Validation result.
- Export hash.

---

## 6. Product Requirements by Workflow Stage

### 6.1 Stage 1: Source Import

The user selects a PDF or DOCX.

Expected behavior:

- Extract text.
- Extract headings, bullet lists, code blocks, tables, and embedded images if possible.
- Preserve page references where useful.
- Store extracted text as the intermediate artifact.

### 6.2 Stage 2: LLM Structuring

The local LLM must produce a structured record, not the ZIP itself.

Expected output:

- Problem title.
- Statement.
- Constraints.
- Inputs/outputs.
- Function signature.
- Sample cases.
- Hidden testcases or testcase references.
- Tags.
- Optional placement metadata.

### 6.3 Stage 3: Human Review

The UI must let a human:

- Correct title and slug.
- Edit extracted content.
- Add or remove testcases.
- Verify language mappings.
- Confirm difficulty.
- Attach stubs and wrappers.
- Set practice placement.

### 6.4 Stage 4: Validation

The app must run deterministic validation rules before export.

### 6.5 Stage 5: ZIP Build

The app must create the exact canonical folder structure and file names.

### 6.6 Stage 6: Optional Import Preflight

The app may run a preflight check against the server-side import rules to detect issues before upload.

---

## 7. System Scope

### In Scope

- Local desktop app.
- Local LLM integration.
- PDF/DOCX ingestion.
- Canonical schema editing.
- ZIP export.
- Validation report.
- Optional dry-run importer check.

### Out of Scope for MVP

- Multi-user server collaboration.
- Cloud-hosted generation.
- Direct production import from the local app.
- Automatic publication without review.

---

## 8. Technical Architecture

### 8.1 High-Level Architecture

The app should have these modules:

1. Ingestion module
   - PDF/DOCX readers.
   - OCR if needed.
2. Extraction module
   - Text segmentation.
   - Layout detection.
3. LLM structuring module
   - Local model prompt orchestration.
4. Review/editor module
   - Form-based schema editor.
5. Validation module
   - Structural and semantic checks.
6. Packaging module
   - Builds canonical ZIP and project artifacts.
7. Export/history module
   - Stores previous versions and hashes.

### 8.2 Recommended Technology Choices

Choose one stack and keep it simple.

Possible local app stacks:

- Electron + React for a rich desktop UI.
- Tauri + React for a lighter desktop app.
- Python + Qt if you want maximum local scripting simplicity.

Recommended general approach:

- UI: React.
- Shell: Electron or Tauri.
- Local inference: Ollama, LM Studio, or a bundled local model runtime.
- Packaging engine: Python or Node.js.

### 8.3 Data Flow

Document -> extraction -> structured schema -> human review -> validation -> canonical ZIP -> checksum -> optional preflight.

---

## 9. Canonical Problem Schema

The local app should maintain one internal schema. This schema is the heart of the solution.

### 9.1 Schema Goals

- Stable.
- Versioned.
- Easy to validate.
- Easy to serialize.
- Easy to map to ZIP files.

### 9.2 Required Schema Version

Use a top-level field:

- `schema_version`

### 9.3 Suggested Schema Fields for Programming Problems

```json
{
  "schema_version": "1.0",
  "problem_type": "code",
  "slug": "sample-two-sum",
  "code": "PRG-0001",
  "title": "Two Sum",
  "difficulty": "Easy",
  "description": "...",
  "description_file": "description.md",
  "constraints": "...",
  "function_name": "two_sum",
  "function_params": ["nums", "target"],
  "return_type": "List[int]",
  "tags": ["array", "hashmap"],
  "languages": ["python", "cpp"],
  "testcases": {
    "python": "testcases/python.json",
    "cpp": "testcases/cpp.json"
  },
  "default_stub": {
    "python": "stubs/python.py"
  },
  "wrappers": {
    "python": "wrappers/python_wrapper.py"
  },
  "category": "Programming",
  "subtopic": ["Basics"],
  "practice_order": 10,
  "image_file": "assets/problem.svg",
  "assets": ["assets/problem.svg"]
}
```

### 9.4 Field Rules

- `slug` must be lowercase, stable, and URL-safe.
- `code` must be unique and max 30 characters.
- `difficulty` must be one of Easy, Medium, Hard.
- `testcases` must be a non-empty map.
- `default_stub` and `wrappers` may be inline source or file references.
- `subtopic` may be a string or list of strings.

---

## 10. Canonical ZIP Specification

This is the format the app must export.

### 10.1 Root Layout

The ZIP must contain:

```text
problems/
  <problem-folder>/
    manifest.json
    description.md
    testcases/
    stubs/
    wrappers/
    assets/
```

### 10.2 Required Folder Rules

- ZIP root must contain `problems/`.
- Each problem must live in one folder under `problems/`.
- Each problem folder must contain `manifest.json`.
- Additional folders are allowed only if referenced in the manifest.

### 10.3 Mandatory Files

For programming problems, the minimum required files are:

- `problems/<problem>/manifest.json`
- At least one testcase JSON file referenced by manifest

### 10.4 Optional Files

- `description.md`
- `stubs/*`
- `wrappers/*`
- `assets/*`

### 10.5 Manifest Location Constraint

Only one manifest per problem folder.

### 10.6 No Path Traversal

The packager must block:

- Absolute paths.
- `../` traversal.
- Symlinks if present in archive output.

---

## 11. Manifest Specification for Programming Problems

### 11.1 Required Fields

- `title`
- `testcases`

### 11.2 Strongly Recommended Fields

- `slug`
- `difficulty`
- `description_file`
- `constraints`
- `function_name`
- `function_params`
- `return_type`
- `tags`

### 11.3 Placement Fields

Use top-level fields only:

- `category`
- `subtopic`
- `practice_order`

### 11.4 Supported Languages

- `python`
- `cpp`
- `java`
- `c`

### 11.5 Testcase Reference Format

Each language key must point to a file path relative to the problem folder.

Example:

```json
"testcases": {
  "python": "testcases/python.json",
  "cpp": "testcases/cpp.json"
}
```

### 11.6 Stub/Wrapper Reference Format

Values can be either:

- Inline source.
- Relative file path.

The app should prefer relative file path references for maintainability.

---

## 12. Testcase JSON Specification

### 12.1 Canonical Shape

```json
{
  "test_cases": [
    {
      "test_case_no": 1,
      "stdin": "1 2 3\n",
      "expected_output": "6",
      "is_visible": true
    }
  ]
}
```

### 12.2 Required Fields Per Case

- `stdin`
- `expected_output`

### 12.3 Optional Fields Per Case

- `test_case_no`
- `is_visible`
- `group`
- `weight`

### 12.4 Validation Rules

- `test_cases` must be a non-empty list.
- Maximum 50 cases per language.
- Each item must be an object.
- Input/output fields should be strings.
- `is_visible` should default to true.

---

## 13. Local LLM Behavior Requirements

### 13.1 Purpose of the LLM

The LLM exists to convert extracted source content into a structured schema.

It must not be the source of truth for final ZIP content.

### 13.2 Required LLM Outputs

- Normalized statement.
- Metadata fields.
- Suggested tags.
- Candidate testcases.
- Suggested stubs and wrappers when derivable.

### 13.3 LLM Constraints

- Output must conform to the schema.
- No invented fields.
- No free-form ZIP paths.
- No unsupported languages.
- No silent assumptions about missing content.

### 13.4 Human-in-the-Loop Rule

The creator must review and approve all LLM output before packaging.

---

## 14. Validation Rules

The validator is non-negotiable.

### 14.1 ZIP Validation

- ZIP size must be under configured limit.
- Root must contain `problems/`.
- Each problem folder must contain `manifest.json`.
- No path traversal.
- No symlinks.
- No duplicate conflicting files.

### 14.2 Manifest Validation

- Title is required.
- Difficulty must be Easy, Medium, or Hard.
- `code` must not exceed 30 characters if provided.
- Function name must be a valid identifier if provided.
- Categories and subtopics must be non-empty if provided.
- Practice order must be a non-negative integer if provided.

### 14.3 Testcase Validation

- Language must be supported.
- Testcase file must exist.
- JSON must parse correctly.
- Testcases array must not be empty.
- Case count must not exceed the limit.

### 14.4 Stub/Wrapper Validation

- File references must resolve within the problem folder.
- Missing referenced files are errors.
- Path-like unresolved values are rejected.

### 14.5 Content Validation

- Optional image file must exist.
- Image extension must be allowed.
- Content must be internally consistent.

---

## 15. Packaging Rules

### 15.1 Packaging Determinism

The same structured input must always produce the same ZIP layout and file naming rules.

### 15.2 File Naming Rules

- Use stable, lowercase folder names.
- Use canonical names for `manifest.json`, `description.md`, and testcase files.
- Keep wrapper and stub file names predictable.

### 15.3 Artifact Outputs

The app should export:

- `package.zip`
- `problem.json` or `problem.yaml`
- `validation-report.json`
- `checksum.sha256`

### 15.4 Reproducibility

Given the same schema and assets, the packager should produce the same archive structure.

---

## 16. User Experience Requirements

### 16.1 Main Screens

1. Create new problem.
2. Import document.
3. Review extracted content.
4. Edit schema.
5. Validate package.
6. Export ZIP.
7. View history.

### 16.2 Usability Requirements

- Easy drag-and-drop import.
- Clear error messages.
- Side-by-side preview of source and structured output.
- Simple editable forms.
- One-click export after approval.

### 16.3 Creator Guidance

The app should tell the user exactly what is missing or invalid.

Do not rely on vague prompts or chatbot memory.

---

## 17. Local-Only and Privacy Requirements

### 17.1 Local Execution

The app must run fully on the user's machine.

### 17.2 Privacy

- Source documents stay local.
- The local model stays local.
- No source document should be sent to external APIs by default.

### 17.3 Optional Network Usage

The app may optionally support:

- Downloading model updates.
- Importing official schema templates.
- Uploading final ZIP to the server.

These should be disabled by default or clearly user-controlled.

---

## 18. Non-Functional Requirements

### 18.1 Performance

- App should open quickly.
- Source extraction should be responsive.
- LLM generation should be bounded and cancellable.

### 18.2 Reliability

- The app should not lose edits if the user navigates away.
- Validation errors should not corrupt the current draft.

### 18.3 Maintainability

- Schema versioning must exist.
- Validation rules should be centralized.
- ZIP builder must be isolated from UI logic.

### 18.4 Portability

- Should run on Windows first.
- Linux and macOS support can follow.

### 18.5 Security

- Reject unsafe paths.
- Restrict file access to selected source files and export directories.
- Treat ZIP content as untrusted until validated.

---

## 19. Recommended Internal APIs for the Local App

The app should have clean internal modules or services.

### 19.1 Ingestion API

- `importDocument(filePath)`
- `extractText(filePath)`
- `extractLayoutHints(filePath)`

### 19.2 Structuring API

- `generateDraftSchema(extractedText)`
- `normalizeToCanonicalSchema(rawDraft)`

### 19.3 Validation API

- `validateSchema(problemSchema)`
- `validateZipLayout(stagingDir)`
- `validateReferences(problemSchema, stagingDir)`

### 19.4 Packaging API

- `buildProblemFolder(problemSchema)`
- `buildZip(projectDir)`
- `writeChecksum(zipPath)`

### 19.5 Review API

- `renderPreview(problemSchema)`
- `showDiff(originalText, structuredFields)`

---

## 20. Suggested Project Structure for the Local App

```text
local-problem-packager/
  app/
    ui/
    core/
    ingestion/
    llm/
    validation/
    packaging/
    export/
  schemas/
    problem.schema.json
    testcase.schema.json
  templates/
    programming/
    mcq/
  samples/
    golden/
  docs/
  tests/
```

### Notes

- Keep schema definitions separate from UI code.
- Keep template ZIP examples in version control.
- Keep validation tests against sample inputs.

---

## 21. Input-to-Output Workflow

### Step 1: Open Document

- User loads PDF or DOCX.

### Step 2: Extract Content

- App extracts the problem statement and metadata hints.

### Step 3: LLM Draft

- Local model fills the schema.

### Step 4: Review

- User verifies fields and testcases.

### Step 5: Validate

- Validator checks the schema and file references.

### Step 6: Package

- App writes the canonical folder tree.

### Step 7: Export

- ZIP and report are saved.

### Step 8: Optional Import Check

- App can run a dry-run against the platform’s current importer contract.

---

## 22. Acceptance Criteria

The tool is considered successful when:

1. Different creators using different source documents still produce the same ZIP structure.
2. The exporter never emits invalid file paths or missing manifests.
3. The validator blocks incomplete or ambiguous outputs before export.
4. The created ZIP imports cleanly into the platform’s bulk import flow.
5. A reviewer can understand and edit the output without opening the ZIP manually.

---

## 23. Risks and Mitigations

### Risk: LLM Hallucination

Mitigation:

- Treat LLM output as draft only.
- Validate everything before export.
- Require human review.

### Risk: Source Documents Are Inconsistent

Mitigation:

- Use a single schema.
- Provide creator templates.
- Add review checkpoints.

### Risk: Too Much Flexibility

Mitigation:

- Freeze the canonical ZIP contract.
- Reject unknown fields or layouts.

### Risk: Local Model Quality Varies

Mitigation:

- Support model selection.
- Provide fallback manual editing.

### Risk: Users Bypass the Official Tool

Mitigation:

- Make the app the easiest path.
- Make server-side validation strict.
- Reject non-canonical uploads.

---

## 24. Rollout Plan

### Phase 1: Specification Freeze

- Freeze the schema.
- Publish one canonical ZIP contract.
- Publish sample packages.

### Phase 2: MVP App

- Build local import, review, validation, and ZIP export.

### Phase 3: Pilot

- Test with a small author group.
- Collect real problem documents.
- Fix ambiguities in the schema.

### Phase 4: Enforced Adoption

- Make the tool mandatory for official packages.
- Reject hand-crafted ZIPs.

### Phase 5: Continuous Improvement

- Improve extraction quality.
- Add better templates.
- Extend to MCQ workflows if needed.

---

## 25. Documentation Deliverables for the Build Agent

If you give this spec to a coding agent, the agent should produce:

1. The local app codebase.
2. Schema definitions.
3. ZIP builder logic.
4. Validation engine.
5. Sample source-to-zip flows.
6. Golden sample projects.
7. Automated tests.
8. A user guide.

---

## 26. Concrete Decision Statement

The final system should be:

- A local, schema-driven, human-reviewed problem authoring app.
- Powered by a local LLM for extraction and draft generation.
- Backed by strict validation.
- Exporting one canonical ZIP format only.

This is the correct balance between flexibility and consistency.
