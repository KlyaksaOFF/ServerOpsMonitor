lint:
	uv run ruff check

lint-fix:
	uv run ruff check --fix

install:
	uv sync

build:
	docker compose up --build -d

bot-start:
	uv run python -m bot.bot_main

api-start:
	sudo uv run python -m api.api_main

docker-logs:
	docker compose logs -f bot

fuser-80:
	sudo fuser -k 80/tcp

api-test:
	uv run pytest