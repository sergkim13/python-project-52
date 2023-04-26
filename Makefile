dev:
	poetry run python manage.py runserver

hooks:
	poetry run pre-commit run --all-files

test:
	poetry run python manage.py test

test-cov:
	poetry run coverage run manage.py test ./tests/
	poetry run coverage report

compose:
	docker compose up -d

stop:
	docker compose down

compose-test:
	docker compose -f docker-compose.test.yaml -p testing up -d

stop-test:
	docker compose -f docker-compose.test.yaml -p testing down
