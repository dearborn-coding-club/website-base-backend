
.PHONY: build_frontend run_frontend run_django run install_dependencies

NPM=pnpm

build_frontend: ## build frontend application
	$(NPM) run build

run_frontend: ## run frontend application
	$(NPM) run dev

run_django: ## run backend application
	python manage.py runserver

run:
	make -j2 run_django run_frontend

# run:
	# ./docker-run.sh
