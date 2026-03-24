lint:
	uv run ruff check

lint-fix:
	uv run ruff check --fix

install:
	uv sync

build:
	docker compose up --build -d

start:
	uv run python main.py

docker-logs:
	docker compose logs -f appwork