from sqlalchemy import String, BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


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

