dev:
	poetry run python manage.py runserver

hooks:
	poetry run pre-commit run --all-files

test:
	poetry run python manage.py test
