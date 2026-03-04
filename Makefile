.PHONY: help install install-dev test test-cov lint format build clean

PYTHON := /usr/local/opt/python@3.13/bin/python3.13
PIP := $(PYTHON) -m pip

help:
	@echo "Commands: install install-dev test test-cov lint format build clean"

install:
	$(PIP) install -e .

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

build:
	$(PYTHON) -m build

clean:
	rm -rf dist/ build/ *.egg-info/ .mypy_cache/ .pytest_cache/
	find . -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null || true
