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

# airflow commands
airflow-db-conn:
	docker compose exec webserver airflow connections add \
	--conn-id postgres1_conn \
	--conn-type postgres \
	--conn-host postgres1 \
	--conn-schema db1 \
	--conn-login usr1 \
	--conn-password pwd1 \
	--conn-port 5432

# python commands
python-test:
	pytest tests