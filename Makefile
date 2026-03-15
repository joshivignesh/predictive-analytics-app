# ── Predictive Analytics App — Developer shortcuts ──────────────
.PHONY: up down build backend frontend lint test clean

up:          ## Start all services
	docker-compose up --build

down:        ## Stop and remove containers
	docker-compose down -v

build:       ## Build all images without starting
	docker-compose build

backend:     ## Run backend only (local venv)
	cd backend && uvicorn app.main:app --reload --port 8000

frontend:    ## Run frontend only
	cd frontend-react && npm start

test-backend: ## Run Python tests
	cd backend && pytest --cov=app tests/

test-frontend: ## Run React tests
	cd frontend-react && npm test -- --watchAll=false

lint-backend: ## Lint Python code
	cd backend && ruff check . && mypy app/

lint-frontend: ## Lint TypeScript/React
	cd frontend-react && npm run lint

clean:       ## Remove Python caches and build artefacts
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +
	find . -type d -name .ruff_cache -exec rm -rf {} +
	rm -rf backend/dist backend/build
