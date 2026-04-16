FROM python:3.13-slim

RUN apt-get update && apt-get install -y make && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY Makefile pyproject.toml ./

RUN make install

COPY . .
