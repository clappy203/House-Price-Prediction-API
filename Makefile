.PHONY: help install train run test lint format typecheck check docker-build docker-up clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "\033[36m%-14s\033[0m %s\n", $$1, $$2}'

install: ## Install package with dev dependencies + pre-commit
	pip install -e ".[dev]"
	pre-commit install

train: ## Train the model artifact
	python -m app.ml.train

run: ## Run the API locally with hot reload
	uvicorn app.main:app --reload

test: ## Run the test suite with coverage
	pytest

lint: ## Lint with ruff
	ruff check .

format: ## Auto-format with black + ruff
	black .
	ruff check --fix .

typecheck: ## Static type checking with mypy
	mypy app

check: lint typecheck test ## Run all quality gates

docker-build: ## Build the Docker image
	docker build -t house-price-api .

docker-up: ## Run via docker compose
	docker compose up --build

clean: ## Remove caches and build artifacts
	rm -rf .pytest_cache .ruff_cache .mypy_cache htmlcov .coverage dist build *.egg-info
