.PHONY: help run test clean install dev docs

help:
	@echo "CLI Game Collection - Available Commands"
	@echo "========================================"
	@echo "make run      - Run the game collection"
	@echo "make test     - Run all tests"
	@echo "make clean    - Clean temporary files"
	@echo "make install  - Install dependencies (if any)"
	@echo "make dev      - Development mode (with checks)"
	@echo "make docs     - View documentation"
	@echo "make lint     - Run code linting"

run:
	@python3 main.py

test:
	@echo "Running tests..."
	@python3 tests/run_tests.py

clean:
	@echo "Cleaning temporary files..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@find . -type f -name "*~" -delete 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf build/ dist/ .pytest_cache/ .coverage htmlcov/ 2>/dev/null || true
	@echo "Cleanup complete!"

install:
	@echo "No external dependencies required!"
	@echo "Python 3.6+ with curses support is sufficient."

dev: clean test
	@echo "Development environment ready!"

docs:
	@echo "Opening documentation..."
	@less README.md

lint:
	@echo "Checking code style..."
	@python3 -m py_compile games/*.py utils/*.py tests/*.py main.py
	@echo "Syntax check passed!"

# Create data directory if it doesn't exist
setup:
	@mkdir -p data/saves
	@echo "Data directories created!"

