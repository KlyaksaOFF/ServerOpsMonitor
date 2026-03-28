from os import getenv

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from db.models import Base

load_dotenv()

engine = create_async_engine(getenv("DATABASE_URL"), echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print('Table was successfully created!')

