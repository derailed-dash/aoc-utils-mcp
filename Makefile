SHELL := /bin/bash

# Install dependencies using uv package manager
install:
	@command -v uv >/dev/null 2>&1 || { echo "uv is not installed. Installing uv..."; curl -LsSf https://astral.sh/uv/0.6.12/install.sh | sh; source $HOME/.local/bin/env; }
	uv sync --dev

# Run unit tests
test:
	@test -n "$(AOC_SESSION_COOKIE)" || (echo "Error: AOC_SESSION_COOKIE is not set. Setup environment before running tests" && exit 1)
	uv run pytest tests

# Run code quality checks (codespell, ruff, mypy)
lint:
	@echo "Running code quality checks..."
	uv sync --dev
	uv run codespell -s
	uv run ruff check . --diff
	uv run mypy .
