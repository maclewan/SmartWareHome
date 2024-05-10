# Docker up
up:
    docker-compose up

# Docker build
build:
    docker-compose up --build

# Migrate
migrate:
    docker-compose run --rm django python manage.py migrate

# Makemigrations
makemigrations:
    docker-compose run --rm django python manage.py makemigrations

# shell-plus
shell_plus:
    docker-compose run --rm django python manage.py shell_plus

# csu
csu:
    docker-compose run --rm django python manage.py createsuperuser --username admin --email admin@admin.com

# black isort
lint:
    black --exclude migrations --line-length 80 ware_home config
    isort --profile black ware_home config

# lint + tests
pytest:
    black --exclude migrations --line-length 80 ware_home config
    isort --profile black ware_home
    docker-compose run --rm django python -m pytest ware_home/tests config
