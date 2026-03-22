from dotenv import load_dotenv
from os import getenv
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

load_dotenv()
TOKEN = (getenv("BOT_TOKEN"))

engine = create_async_engine(getenv('PSQL'), echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)
