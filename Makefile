makemigrations:
	alembic revision  --autogenerate -m 'initial commit'

migrate:
	alembic upgrade heads

down-migrate:
	alembic downgrade

current-mig:
	alembic current
extract:
	pybabel extract --input-dirs=. -o locales/messages.pot

init:
	pybabel init -i locales/messages.pot -d locales -D messages -l en
	pybabel init -i locales/messages.pot -d locales -D messages -l uz


compile:
	pybabel compile -d locales -D messages

update:
	pybabel update -d locales -D messages -i locales/messages.pot

country_script:
	python3 utils/country_script.py

createsuperuser:
	python3  utils/superuser.py