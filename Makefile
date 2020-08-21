serve:

	poetry run ./manage.py runserver --asgi

createdb:
	createuser -s dj_asgi_utils
	createdb dj_asgi_utils

dropdb:
	dropdb --if-exists test_dj_asgi_utils
	dropdb --if-exists dj_asgi_utils
	dropuser --if-exists dj_asgi_utils

migrate:
	poetry run ./manage.py migrate

seeds:
	poetry run ./manage.py createsuperuser --username=admin --email=admin@example.com

db: dropdb createdb migrate

lint:
	poetry run black .
	poetry run isort .

test:
	poetry run pytest


shell:
	poetry run ./manage.py shell_plus