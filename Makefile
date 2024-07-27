
.PHONY: run-django run run-docker


run-django: ## run backend application
	python manage.py runserver

# run:
# 	make -j2 run_django run_frontend

run:
	make -j2 run_django run_frontend

run-docker:
	./docker-run.sh
