import asyncio

import uvicorn
from fastapi import FastAPI

from api.routes import login, server
from db.db import init_db

app = FastAPI()

app.include_router(server.router)
app.include_router(login.router)


async def main() -> None:
    await init_db()
    uvicorn.run("api.api_main:app",
                      host='127.0.0.1',
                      port=80, reload=True)


if __name__ == "__main__":
    asyncio.run(main())