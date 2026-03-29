import uvicorn
from fastapi import FastAPI
from routes import server

app = FastAPI()

app.include_router(server.router)


if __name__ == "__main__":
    uvicorn.run("api_main:app", host='127.0.0.0', port=8111, reload=True)