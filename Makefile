.PHONY: help install install-dev clean lint format type-check test test-cov run build docker-build docker-run all

# Default target
.DEFAULT_GOAL := help

# Python and UV executables
PYTHON := python3
UV := uv
PACKAGE_NAME := video_translator

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

##@ General

help: ## Display this help message
	@echo "$(BLUE)═══════════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)  Video Translator - Production-Ready Makefile$(NC)"
	@echo "$(BLUE)═══════════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"; printf "Usage:\n  make $(YELLOW)<target>$(NC)\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  $(BLUE)%-20s$(NC) %s\n", $$1, $$2 } /^##@/ { printf "\n$(GREEN)%s$(NC)\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(BLUE)═══════════════════════════════════════════════════════════════$(NC)"

##@ Installation

install: ## Install production dependencies using uv
	@echo "$(GREEN)Installing production dependencies with uv...$(NC)"
	@command -v $(UV) >/dev/null 2>&1 || { echo "$(RED)Error: uv is not installed. Install from https://github.com/astral-sh/uv$(NC)"; exit 1; }
	$(UV) pip install -e .
	@echo "$(GREEN)✓ Production dependencies installed successfully$(NC)"

install-dev: ## Install all dependencies including development tools
	@echo "$(GREEN)Installing all dependencies (production + dev) with uv...$(NC)"
	@command -v $(UV) >/dev/null 2>&1 || { echo "$(RED)Error: uv is not installed. Install from https://github.com/astral-sh/uv$(NC)"; exit 1; }
	$(UV) pip install -e ".[dev]"
	@echo "$(GREEN)✓ All dependencies installed successfully$(NC)"

sync: ## Synchronize dependencies using uv sync
	@echo "$(GREEN)Synchronizing dependencies with uv...$(NC)"
	@command -v $(UV) >/dev/null 2>&1 || { echo "$(RED)Error: uv is not installed. Install from https://github.com/astral-sh/uv$(NC)"; exit 1; }
	$(UV) sync
	@echo "$(GREEN)✓ Dependencies synchronized$(NC)"

##@ Code Quality

lint: ## Run code linting with ruff
	@echo "$(GREEN)Running ruff linter...$(NC)"
	$(UV) run ruff check $(PACKAGE_NAME) tests
	@echo "$(GREEN)✓ Linting completed$(NC)"

lint-fix: ## Run code linting with automatic fixes
	@echo "$(GREEN)Running ruff linter with auto-fix...$(NC)"
	$(UV) run ruff check --fix $(PACKAGE_NAME) tests
	@echo "$(GREEN)✓ Linting and fixes completed$(NC)"

format: ## Format code with black and isort
	@echo "$(GREEN)Formatting code with black...$(NC)"
	$(UV) run black $(PACKAGE_NAME) tests
	@echo "$(GREEN)Sorting imports with isort...$(NC)"
	$(UV) run isort $(PACKAGE_NAME) tests
	@echo "$(GREEN)✓ Code formatting completed$(NC)"

format-check: ## Check code formatting without making changes
	@echo "$(GREEN)Checking code format...$(NC)"
	$(UV) run black --check $(PACKAGE_NAME) tests
	$(UV) run isort --check-only $(PACKAGE_NAME) tests
	@echo "$(GREEN)✓ Format check completed$(NC)"

type-check: ## Run static type checking with mypy
	@echo "$(GREEN)Running mypy type checker...$(NC)"
	$(UV) run mypy $(PACKAGE_NAME)
	@echo "$(GREEN)✓ Type checking completed$(NC)"

##@ Testing

test: ## Run tests with pytest
	@echo "$(GREEN)Running tests...$(NC)"
	$(UV) run pytest tests/ -v
	@echo "$(GREEN)✓ Tests completed$(NC)"

test-cov: ## Run tests with coverage report
	@echo "$(GREEN)Running tests with coverage...$(NC)"
	$(UV) run pytest tests/ -v --cov=$(PACKAGE_NAME) --cov-report=term-missing --cov-report=html
	@echo "$(GREEN)✓ Coverage report generated in htmlcov/index.html$(NC)"

test-watch: ## Run tests in watch mode
	@echo "$(GREEN)Running tests in watch mode...$(NC)"
	$(UV) run pytest-watch tests/

##@ Application

run: ## Run the Video Translator application
	@echo "$(GREEN)Starting Video Translator...$(NC)"
	$(UV) run video-translator

dev: install-dev ## Setup development environment
	@echo "$(GREEN)Development environment ready!$(NC)"
	@echo "$(YELLOW)Run 'make run' to start the application$(NC)"

##@ Build & Distribution

build: clean ## Build distribution packages
	@echo "$(GREEN)Building distribution packages...$(NC)"
	$(UV) build
	@echo "$(GREEN)✓ Build completed - packages in dist/$(NC)"

publish-test: build ## Publish to Test PyPI
	@echo "$(YELLOW)Publishing to Test PyPI...$(NC)"
	$(UV) publish --repository testpypi
	@echo "$(GREEN)✓ Published to Test PyPI$(NC)"

publish: build ## Publish to PyPI
	@echo "$(RED)Publishing to PyPI...$(NC)"
	@read -p "Are you sure you want to publish to PyPI? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		$(UV) publish; \
		echo "$(GREEN)✓ Published to PyPI$(NC)"; \
	else \
		echo "$(YELLOW)Publishing cancelled$(NC)"; \
	fi

##@ Cleanup

clean: ## Remove build artifacts and cache files
	@echo "$(GREEN)Cleaning build artifacts and cache...$(NC)"
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .ruff_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -f audio.wav test.wav
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
	find . -type f -name '*~' -delete
	@echo "$(GREEN)✓ Cleanup completed$(NC)"

clean-videos: ## Remove generated translated video files
	@echo "$(YELLOW)Removing generated video files...$(NC)"
	rm -f video_translated_*.mp4
	@echo "$(GREEN)✓ Video files cleaned$(NC)"

clean-all: clean clean-videos ## Remove all generated files including videos
	@echo "$(GREEN)✓ Complete cleanup finished$(NC)"

##@ Docker (Optional)

docker-build: ## Build Docker image
	@echo "$(GREEN)Building Docker image...$(NC)"
	docker build -t video-translator:latest .
	@echo "$(GREEN)✓ Docker image built$(NC)"

docker-run: ## Run application in Docker container
	@echo "$(GREEN)Running Docker container...$(NC)"
	docker run -p 7860:7860 video-translator:latest

##@ CI/CD

ci: lint format-check type-check test ## Run all CI checks (lint, format, type-check, test)
	@echo "$(GREEN)✓ All CI checks passed!$(NC)"

pre-commit: format lint type-check test ## Run pre-commit checks (format, lint, type-check, test)
	@echo "$(GREEN)✓ Pre-commit checks passed!$(NC)"

##@ Composite Targets

all: clean install-dev lint format type-check test ## Run complete workflow: clean, install, lint, format, type-check, test
	@echo "$(GREEN)✓ Complete workflow finished successfully!$(NC)"

check: lint format-check type-check ## Quick check: lint, format-check, type-check
	@echo "$(GREEN)✓ Quick checks passed!$(NC)"

##@ Information

info: ## Display project information
	@echo "$(BLUE)═══════════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)Project Information$(NC)"
	@echo "$(BLUE)═══════════════════════════════════════════════════════════════$(NC)"
	@echo "$(YELLOW)Package:$(NC)       $(PACKAGE_NAME)"
	@echo "$(YELLOW)Python:$(NC)        $$($(PYTHON) --version)"
	@echo "$(YELLOW)UV:$(NC)            $$($(UV) --version 2>/dev/null || echo 'Not installed')"
	@echo "$(YELLOW)Working Dir:$(NC)   $$(pwd)"
	@echo "$(BLUE)═══════════════════════════════════════════════════════════════$(NC)"
