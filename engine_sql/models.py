from typing import List, Optional
from sqlalchemy import create_engine, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'user_accounts'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[float] = mapped_column(primary_key=True)
    server_list_id: Mapped[float] = mapped_column()

class ServerList(Base):
    __tablename__ = 'server_lists'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(10))
    ip: Mapped[float] = mapped_column()

