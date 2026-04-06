# ServerOps Monitor
![CI](https://github.com/KlyaksaOFF/ServerOpsMonitor/actions/workflows/workflow.yml/badge.svg)

ServerOps Monitor

A professional Telegram bot and web interface designed for monitoring and managing Linux servers using Ansible. This tool allows you to track server health and execute remote checks directly from your mobile device or browser.
🚀 Key Features

    Telegram Management: Add, view servers via a native Telegram interface.

    Automated Health Checks: Run ping and uptime checks using Ansible modules.

    Web Dashboard: Built-in FastAPI server providing a web UI for server management.

    Asynchronous Architecture: Fully async operations using aiogram, FastAPI, and SQLAlchemy.

    Secure Environment: Containerized deployment with Docker and automated CI/CD via GitHub Actions.

🛠 Tech Stack

    Language: Python 3.13

    Frameworks:

        Aiogram 3.x (Telegram Bot)

        FastAPI (Web API & UI)

    Database: PostgreSQL with SQLAlchemy 2.0 (AsyncPG)

    Automation: Ansible Core

    Infrastructure: Docker, Docker Compose

    Code Quality: Ruff (Linter)

📦 Installation & Setup
Prerequisites

    Docker & Docker Compose installed.

    A Telegram Bot Token from @BotFather.

Quick Start

    Clone the repository:
    Bash

    git clone https://github.com/KlyaksaOFF/ServerOpsMonitor.git
    cd ServerOpsMonitor

    Configure Environment:
    Create a .env file from the template:
    Bash

    cp .env.example .env

    Insert your BOT_TOKEN and database credentials.

    Deploy with Docker:
    Bash

    docker-compose up -d --build

📋 Usage Guide

    Start the Bot: Send the /start command to your bot in Telegram.

    Add a Server: Select "Add Server" and follow the prompts to enter the IP address and password.

    Run Monitoring: Navigate to "Server List", select a host, and trigger a check.

    Web Access: Open http://localhost:80 to access the FastAPI dashboard.

🏗 Project Structure

    bot/: Core Telegram bot initialization and polling logic.

    api/: FastAPI routes, logic, and HTML templates (Jinja2).

    handlers/: Telegram message handlers and Finite State Machine (FSM) logic.

    services/: Ansible Runner integration for executing remote tasks.

    repositories/: Database abstraction layer (CRUD operations).

    db/: SQLAlchemy models and database connection setup.

    utils/: Helper functions like IP address validation.
