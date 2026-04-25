# Contributing

## Prerequisites

1. Node.js 20+
2. pnpm 9+
3. Rust stable toolchain
4. Python 3.11+

## Setup

1. Install JS dependencies: `pnpm install`
2. Check Rust workspace: `cargo check --workspace`
3. Run Python tests: `pytest`

## MVP priorities

1. MCQ schema and validator
2. Deterministic packager
3. Ingestion sidecar for PDF/DOCX/MD/TXT
4. Tauri flow: import -> validate -> approve -> export
