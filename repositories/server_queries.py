from sqlalchemy import select

from db.models import Admins


async def get_admin_by_user_id(user_id, session):
    process_filter_current_admin = await session.execute(
        select(Admins).filter_by(user_id=user_id, admin=True))

    result_current_admin = process_filter_current_admin.scalar_one_or_none()
    return result_current_admin