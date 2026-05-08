from sqlalchemy import insert, select

from db.db import async_session
from db.models import Admins
from repositories.server_queries import get_admin_by_user_id


async def check_admin_user_id(user_id):
    async with async_session() as session:
        filter_process = await session.execute(
            select(Admins).filter_by(user_id=user_id))
        user = filter_process.scalar_one_or_none()
        return user


async def add_new_admin(current_admin_id, new_admin_id):
    async with async_session() as session:
        result_current_admin_id = await get_admin_by_user_id(
            current_admin_id, session)
        existing_new_admin = await get_admin_by_user_id(
            new_admin_id, session)

        if result_current_admin_id and not existing_new_admin:
            await session.execute(
                insert(Admins).values(user_id=new_admin_id))
            await session.commit()
            return True

        return False


async def all_admin_users():
    async with async_session() as session:
        process_filter = await session.execute(
        select(Admins))
        users = process_filter.scalars().all()
        return users


async def remove_user_admin(user_id):
    async with async_session() as session:
        result = await session.execute(select(Admins).where(
            Admins.user_id == user_id))
        user = result.scalar_one_or_none()

        if user:
            await session.delete(user)
            await session.commit()