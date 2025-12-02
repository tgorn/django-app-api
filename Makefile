
# Docker compoose lint
lint:
	docker-compose run --rm app sh -c "flake8"

start_project:
	docker-compose run --rm app sh -c "django-admin startproject app . "

run:
	docker-compose up 