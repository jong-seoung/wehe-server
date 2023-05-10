local:
	docker-compose -f docker-compose-dev.yml up
down:
	docker-compose -f docker-compose-dev.yml down
makemigrations:
	docker-compose -f docker-compose-dev.yml exec app python manage.py makemigrations
migrate:
	docker-compose -f docker-compose-dev.yml exec app python manage.py migrate
