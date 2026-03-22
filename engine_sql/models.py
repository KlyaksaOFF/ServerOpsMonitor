import asyncio
from sqlalchemy import String, BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from aiogram.fsm.state import StatesGroup, State
from dotenv import load_dotenv
from os import getenv

load_dotenv()
TOKEN = (getenv("BOT_TOKEN"))

engine = create_async_engine(getenv('PSQL'), echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


class AddServer(StatesGroup):
    waiting_for_ip = State()
    waiting_for_password = State()

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'user_accounts'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    server_list_id: Mapped[float] = mapped_column(nullable=True)

class ServerList(Base):
    __tablename__ = 'server_lists'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(10))
    ip: Mapped[str] = mapped_column(String(45))
    password: Mapped[str] = mapped_column(String(50))
    user_id: Mapped[int] = mapped_column(BigInteger)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print('Table was successfully created!')


if __name__ == "__main__":
    asyncio.run(init_db())