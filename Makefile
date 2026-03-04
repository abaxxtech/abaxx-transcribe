.PHONY: help install install-dev test test-cov lint format format-check type-check build clean

PYTHON := $(shell pwd)/.venv/bin/python3.13
PIP    := $(shell pwd)/.venv/bin/pip

help:
	@echo "abaxx-transcribe dev commands:"
	@echo "  install      Install package in venv (editable)"
	@echo "  install-dev  Install with dev dependencies"
	@echo "  test         Run unit tests (fast only)"
	@echo "  test-cov     Run tests with coverage"
	@echo "  lint         Run flake8 linter"
	@echo "  format       Format with black"
	@echo "  type-check   Run mypy"
	@echo "  build        Build distribution packages"
	@echo "  clean        Remove build artifacts"

install:
	$(PIP) install -e . --no-deps

install-dev:
	$(PIP) install -e . -r requirements-dev.txt

test:
	$(PYTHON) -m pytest tests/ -v -m "not slow and not integration"

test-cov:
	$(PYTHON) -m pytest tests/ -v --cov=transcribe_and_diarize --cov-report=term-missing

lint:
	$(PYTHON) -m flake8 transcribe_and_diarize/ tests/

format:
	$(PYTHON) -m black transcribe_and_diarize/ tests/

format-check:
	$(PYTHON) -m black --check transcribe_and_diarize/ tests/

type-check:
	$(PYTHON) -m mypy transcribe_and_diarize/

build:
	$(PYTHON) -m build

clean:
	rm -rf dist/ build/ *.egg-info/ .mypy_cache/ .pytest_cache/ htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
