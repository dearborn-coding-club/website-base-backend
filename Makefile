.PHONY: run-django run run-docker setup pull-repos help

help: ## Show this help message
	@echo "Available commands:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup: ## Setup the complete development environment
	./setup.sh

pull-repos: ## Pull auth and frontend repositories
	./pull-repos.sh

run-django: ## Run backend application
	python manage.py runserver

run: ## Run backend application (default)
	make -j2 run-django

run-docker: ## Run with Docker (legacy)
	./docker-run.sh

docker-up: ## Start Docker Compose development environment
	docker-compose up --build

docker-down: ## Stop Docker Compose environment
	docker-compose down

docker-logs: ## View Docker Compose logs
	docker-compose logs -f

docker-full: ## Start full environment (backend + frontend + auth)
	docker-compose -f docker-compose.full.yml up --build

docker-prod: ## Start production-like environment
	docker-compose -f docker-compose.production.yml up --build

migrate: ## Run Django migrations
	python manage.py migrate

shell: ## Open Django shell
	python manage.py shell

superuser: ## Create Django superuser
	python manage.py createsuperuser

test: ## Run tests
	python manage.py test

lint: ## Run linting
	flake8 .

clean: ## Clean up Python cache files
	find . -type d -name __pycache__ -delete
	find . -name "*.pyc" -delete

fix-docker: ## Fix frontend Docker build issues
	./fix-frontend-docker.sh
