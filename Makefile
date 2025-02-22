# docker commands
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