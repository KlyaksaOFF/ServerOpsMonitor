import asyncio
from os import getenv

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from api.routes import admin, login, server
from db.db import init_db

app = FastAPI()
host = getenv("HOST")
port = int(getenv("PORT"))
app.include_router(server.router)
app.include_router(login.router)
app.include_router(admin.router)

load_dotenv()


async def main() -> None:
    await init_db()
    uvicorn.run("api.api_main:app",
                      host=host,
                      port=port, reload=True)


if __name__ == "__main__":
    asyncio.run(main())