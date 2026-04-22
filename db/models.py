from sqlalchemy import BigInteger, Boolean, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class ServerList(Base):
    __tablename__ = 'server_lists'

    id: Mapped[int] = mapped_column(primary_key=True)
    ip: Mapped[str] = mapped_column(String(45))
    password: Mapped[str] = mapped_column(String(50))
    user_id: Mapped[int] = mapped_column(BigInteger)
    ping: Mapped[str] = mapped_column(String(20), nullable=True)
    uptime: Mapped[str] = mapped_column(String(100), nullable=True)
    autocheck: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )

class Admins(Base):
    __tablename__ = 'admins'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    admin: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )