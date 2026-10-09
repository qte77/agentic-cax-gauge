# Requires GNU Make >= 3.82 for .ONESHELL
# macOS ships 3.81: brew install make, then use gmake
ifeq ($(filter oneshell,$(.FEATURES)),)
$(error GNU Make >= 3.82 required. macOS: brew install make, then use gmake)
endif

.SILENT:
.ONESHELL:
.PHONY: \
	setup_uv setup setup_cad \
	autofix lint type test test_cov check_complexity validate check_docs check_links \
	help
.DEFAULT_GOAL := help


# -- config --
VERBOSE ?= 0
ifeq ($(VERBOSE),0)
RUFF_QUIET := --quiet
PYTEST_QUIET := -q --tb=short --no-header
PYRIGHT_QUIET := > /dev/null
else
RUFF_QUIET :=
PYTEST_QUIET :=
PYRIGHT_QUIET :=
endif

MD_FILES := "*.md" "docs/**/*.md"


# MARK: SETUP


setup_uv: ## Install uv package manager (if missing)
	if command -v uv > /dev/null 2>&1; then
		echo "uv already installed: $$(uv --version)"
	else
		echo "Installing uv ..."
		curl --proto '=https' --tlsv1.2 -LsSf https://astral.sh/uv/install.sh | sh
		echo "NOTE: restart your shell or run 'source $$HOME/.local/bin/env' to add uv to PATH"
	fi

setup: setup_uv ## Install runtime + dev + test dependencies
	uv sync

setup_cad: setup_uv ## Install build123d (optional cad extra)
	uv sync --extra cad


# MARK: QUALITY


autofix: ## Auto-format and fix lint issues (use before committing)
	uv run ruff format . $(RUFF_QUIET) && uv run ruff check . --fix $(RUFF_QUIET)

lint: ## Check formatting + lint (fails on issues, does not fix)
	uv run ruff format --check . $(RUFF_QUIET) && uv run ruff check . $(RUFF_QUIET)

type: ## Run pyright (strict) type checking
	uv run pyright src $(PYRIGHT_QUIET)

test: ## Run tests (cad/browser-marked tests excluded by default)
	uv run pytest $(PYTEST_QUIET)

test_cov: ## Run tests with coverage report
	uv run pytest --cov=caxgauge --cov-report=term-missing $(PYTEST_QUIET)

check_complexity: ## Check cognitive complexity (max 15/function)
	uv run complexipy src/caxgauge/ --max-complexity-allowed 15

validate: lint type test check_complexity ## Full Python gate — the exact CI gate (validate.yaml)
	echo "validate: PASS (lint + type + test + complexity)"

# Docs/link checks report SKIP, never PASS, when their tool is absent (verification-honesty).
check_docs: ## Lint markdown (reads .markdownlint.json); SKIP if markdownlint-cli2 is absent
	if command -v markdownlint-cli2 > /dev/null 2>&1; then
		markdownlint-cli2 $(MD_FILES)
	else
		echo "check_docs: SKIP — markdownlint-cli2 not installed (npm install -g markdownlint-cli2)"
	fi

check_links: ## Check links (reads .lychee.toml, needs network); SKIP if lychee is absent
	if command -v lychee > /dev/null 2>&1; then
		lychee --config .lychee.toml .
	else
		echo "check_links: SKIP — lychee not installed (https://github.com/lycheeverse/lychee/releases)"
	fi


# MARK: HELP


help: ## Show available recipes grouped by section
	echo "Usage: make [recipe]"
	echo ""
	awk '/^# MARK:/ { \
		section = substr($$0, index($$0, ":")+2); \
		printf "\n\033[1m%s\033[0m\n", section \
	} \
	/^[a-zA-Z0-9_-]+:.*?##/ { \
		helpMessage = match($$0, /## (.*)/); \
		if (helpMessage) { \
			recipe = $$1; \
			sub(/:/, "", recipe); \
			printf "  \033[36m%-18s\033[0m %s\n", recipe, substr($$0, RSTART + 3, RLENGTH) \
		} \
	}' $(MAKEFILE_LIST)
