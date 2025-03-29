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

# docker-init:
# 	chmod +x ./scripts/setup_metabase_db.sh
# 	docker compose up -d || exit 1
# 	# Wait for postgres1 and postgres2 to be ready
# 	for db in postgres1 postgres2; do \
# 		while ! docker compose exec -T $$db pg_isready -U usr$${db:7} -d db$${db:7}; do \
# 			sleep 1; \
# 		done \
# 	done
# 	docker compose run --rm postgres1 /bin/bash -c "./scripts/setup_metabase_db.sh" || exit 1
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