.PHONY: build
build:
	@docker-compose build

.PHONY: down
down:
	@docker-compose down

.PHONY: logs
logs:
	@docker-compose logs --follow

.PHONY: up
up:
	@docker-compose up

.PHONY: up-silent
up-silent:
	@docker-compose up -d
