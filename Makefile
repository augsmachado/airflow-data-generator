# venv commands
venv-create:
	python3 -m venv venv

venv-activate:
	source venv/bin/activate

venv-deactivate:
	deactivate

venv-install:
	pip install --upgrade pip
	pip install -r requirements.txt --upgrade

venv-freeze:
	pip freeze > requirements.txt

# docker commands
docker-init:
	docker compose up -d

docker-rebuild:
	docker compose up --build -d

docker-verify:
	docker ps

docker-logs:
	docker compose logs

docker-down:
	docker compose down