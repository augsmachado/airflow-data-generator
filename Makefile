# venv commands
venv-create:
	python3 -m venv venv

venv-activate:
	source venv/bin/activate

venv-deactivate:
	deactivate

venv-install:
	pip3 install --upgrade pip
	pip3 install -r requirements.txt --upgrade

venv-freeze:
	pip3 freeze > requirements.txt

# docker commands
docker-build:
	docker compose build

docker-init:
	docker compose up -d

docker-rebuild:
	docker compose up -d --build

docker-verify:
	docker ps

docker-logs:
	docker compose logs

docker-down:
	docker compose down

# python commands
python-test:
	pytest tests