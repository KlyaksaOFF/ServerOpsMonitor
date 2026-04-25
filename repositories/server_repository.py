from aiogram.fsm.context import FSMContext
from sqlalchemy import distinct, func, select, update

from db.db import async_session
from db.models import Admins, ServerList
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


async def remove_server_by_server_id(server_id):
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


async def get_all_servers_autocheck():
    async with async_session() as session:
        result = await session.execute(
    select(ServerList).filter_by(autocheck=True)
        )
        servers = result.scalars().all()

        return servers


async def process_function_autocheck(server_id):
    async with async_session() as session:
        filter_process = await session.execute(
            select(ServerList).filter_by(id=server_id)
        )

        server = filter_process.scalar_one_or_none()

        match server.autocheck:
            case True:
                server.autocheck = False
                await session.commit()
            case False:
                server.autocheck = True
                await session.commit()


async def state_autocheck_server(server_id):
    async with async_session() as session:
        filter_process = await session.execute(
            select(ServerList).filter_by(id=server_id, autocheck=False)
        )

        server = filter_process.scalar_one_or_none()

        return '❌Now AutoCheck off❌' if server else '✅Now AutoCheck on✅'


async def count_unique_users():
    async with async_session() as session:
        filter_process = await session.execute(
            select(func.count(distinct(ServerList.user_id))))

        unique_users = filter_process.scalar()

        return unique_users


async def count_unique_servers():
    async with async_session() as session:
        filter_process = await session.execute(
            select(func.count(distinct(ServerList.ip))))

        unique_servers = filter_process.scalar()

        return unique_servers


async def check_admin_user_id(user_id):
    async with async_session() as session:
        filter_process = await session.execute(
            select(Admins).filter_by(user_id=user_id))

        user = filter_process.scalar_one_or_none()

        return user


async def all_users_id():
    async with async_session() as session:
        filter_process = await session.execute(
            select(ServerList.user_id).distinct())

        users_ids = filter_process.scalars().all()

        return users_ids


async def all_servers_ip():
    async with async_session() as session:
        filter_process = await session.execute(select(ServerList.ip).distinct())

        servers_ip = filter_process.scalars().all()

        return servers_ip


async def remove_all_where_ip(server_ip):
    async with async_session() as session:
        result = await session.execute(
            select(ServerList).filter_by(ip=server_ip)
        )

        servers = result.scalars().all()

        if servers:
            for server in servers:
                await session.delete(server)
            await session.commit()
