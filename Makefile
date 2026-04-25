.PHONY: help
help:
	@echo "Common tasks:"
	@echo "  make js-install      # Install JS workspace deps"
	@echo "  make rust-check      # Run Rust workspace checks"
	@echo "  make py-test         # Run Python sidecar tests"

.PHONY: js-install
js-install:
	pnpm install

.PHONY: rust-check
rust-check:
	cargo check --workspace

.PHONY: py-test
py-test:
	pytest
