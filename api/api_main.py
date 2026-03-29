import uvicorn
from fastapi import FastAPI
from routes import login, server

app = FastAPI()

app.include_router(server.router)
app.include_router(login.router)


if __name__ == "__main__":
    uvicorn.run("api_main:app", host='127.0.0.1', port=80, reload=True)