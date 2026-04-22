migrate:
	docker compose run app python manage.py migrate

format:
	docker compose run app /bin/sh -c "ruff format && ruff check --fix && mypy ."

test:
	docker compose run app python manage.py test $(TEST)

run:
	docker compose up app
