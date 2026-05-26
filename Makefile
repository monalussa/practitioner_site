run:
	python manage.py runserver

migrate:
	python manage.py migrate

seed:
	python manage.py seed_content

test:
	python manage.py test

collect:
	python manage.py collectstatic --noinput
