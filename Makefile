lint:
	uv run ruff check

lint-fix:
	uv run ruff check --fix

install:
	uv sync

build:
	docker compose up --build -d

docker-run:
	docker compose up -d

bot-start:
	uv run python -m bot.bot_main

api-start:
	sudo uv run python -m api.api_main

docker-logs:
	docker compose logs -f bot

fuser-80:
	sudo fuser -k 80/tcp

test-api:
	uv run pytest api

test-bot:
	uv run pytest bot

make key:
	python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"