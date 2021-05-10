.PHONY: build
build:
	@docker-compose build

.PHONY: down
down:
	@docker-compose down

.PHONY: grpc
grpc:
	@docker-compose run --rm poc-bff-fastapi python -m grpc_tools.protoc --proto_path=app/grpc/proto --python_out=app/grpc/src --grpc_python_out=app/grpc/src app/grpc/proto/*.proto

.PHONY: logs
logs:
	@docker-compose logs --follow

.PHONY: up
up:
	@docker-compose up

.PHONY: up-grpc
up-grpc:
	@docker-compose exec poc-bff-fastapi python app/server.py

.PHONY: up-silent
up-silent:
	@docker-compose up -d
