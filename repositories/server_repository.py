from aiogram.fsm.context import FSMContext
from sqlalchemy import select

from db.db import async_session
from db.models import ServerList
from utils.validate_ip import result_ip


async def get_server_by_id(server_id):
    async with async_session() as session:
        filter_result = await session.execute(
            select(ServerList).filter_by(id=server_id)
        )

        return filter_result.scalar_one_or_none()


async def create_server(ip, password, user_id):
    async with async_session() as session:

        server = ServerList(
            password=password,
            user_id=user_id,
            ip=ip,
        )

        session.add(server)
        await session.commit()


async def process_add_server(server_ip, user_id, state: FSMContext):
    async with async_session() as session:
        filter_result = await session.execute(select(ServerList).filter_by(
            ip=server_ip, user_id=user_id)
        )

        server = filter_result.scalar_one_or_none()

        result = await result_ip(server, server_ip, state)
        return result