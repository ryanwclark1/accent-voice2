# 🎯 Project Automation Makefile
.PHONY: install lint format test coverage security deps check-all

install:  ## 🔧 Install dependencies
	@echo "📦 Installing dependencies..."
	uv pip install -e .[dev]

lint:  ## 🔍 Run Ruff linting
	@echo "🔎 Running lint checks..."
	ruff check .

format:  ## 🎨 Format code with Ruff & Djlint
	@echo "🎨 Formatting code..."
	ruff format .
	djlint templates/ --reformat

test:  ## 🧪 Run tests with pytest
	@echo "🧪 Running tests..."
	pytest tests/

coverage:  ## 📊 Run coverage tests
	@echo "📊 Checking test coverage..."
	coverage run -m pytest
	coverage report -m
	coverage html
	@echo "✅ Coverage report generated in 'coverage_html_report'"

security:  ## 🔒 Run security scans with Bandit
	@echo "🔒 Running security checks..."
	bandit -r src/

deps:  ## 🗂️ Check for missing/unused dependencies
	@echo "🗂️ Checking dependencies..."
	deptry .

refactor:  ## 🛠️ Run Refurb to detect bad patterns
	@echo "🛠️ Running code quality checks..."
	refurb .

check-all: lint format test coverage security deps refactor  ## ✅ Run all checks
	@echo "🚀 Running all quality checks..."
