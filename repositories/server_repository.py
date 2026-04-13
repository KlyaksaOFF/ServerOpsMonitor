from aiogram.fsm.context import FSMContext
from sqlalchemy import select, update

from db.db import async_session
from db.models import ServerList
from utils.validate_ip import result_ip_api, result_ip_telegram


async def list_user_connected_servers(user_id):
    async with async_session() as session:

        filter_result = await session.execute(
            select(ServerList).filter_by(user_id=user_id)
        )

        servers = filter_result.scalars().all()
    return servers


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

        result = await result_ip_telegram(server, server_ip, state)
        return result


async def added_check_in_table_server(server, ping, uptime):
    async with async_session() as session:
        await session.execute(update(ServerList).where(ServerList.ip
                                                       == server.ip)
        .values(ping=ping, uptime=uptime))
        await session.commit()


async def remove_server_by_id(server_id):
    server = await get_server_by_id(server_id)
    async with async_session() as session:
        await session.delete(server)
        await session.commit()


async def have_user_server(user_id, server_ip):
    async with async_session() as session:
        filter_result = await session.execute(select(ServerList).filter_by(
            ip=server_ip, user_id=user_id)
        )

        server = filter_result.scalar_one_or_none()
        result_validate_ip = await result_ip_api(
            server=server,
            server_ip=server_ip
        )
        return result_validate_ip