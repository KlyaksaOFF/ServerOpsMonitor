lint:
	uv run ruff check

lint-fix:
	uv run ruff check --fix

install:
	uv sync

build:
	docker compose up --build -d

bot start:
	uv run python bot_main.py

api start:
	uv run python api_main.py

docker-logs:
	docker compose logs -f appwork