import logging

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy import select

from db.db import async_session
from db.models import ServerList
from handlers.fsm_states import AddServer
from services.server_check import (
    result_check_server,
)
from texts.texts import (
    ENTER_IP,
    ERROR_INVALID_IP,
    NOT_SERVER,
    SEND_PASSWORD,
    SERVER_CREATED,
    SERVER_IN_YOUR_LIST,
)
from utils.validate_ip import result_ip

router = Router()


@router.message(F.text.lower() == 'add server')
async def add_server_start(message: types.Message, state: FSMContext):
    await message.answer(ENTER_IP)
    await state.set_state(AddServer.waiting_for_ip)


@router.message(AddServer.waiting_for_ip)
async def process_ip(message: types.Message, state: FSMContext):
    async with async_session() as session:
        server_ip = message.text.strip()
        filter_result = await session.execute(select(ServerList).filter_by(
            ip=server_ip, user_id=message.from_user.id)
        )

        server = filter_result.scalar_one_or_none()

        result = await result_ip(server, server_ip, state)
        if result == "valid_ip":
            await message.answer(SEND_PASSWORD)
        elif result == "invalid_ip":
            await message.answer(ERROR_INVALID_IP)
        else:
            await message.answer(SERVER_IN_YOUR_LIST)


@router.message(AddServer.waiting_for_password)
async def process_password(message: types.Message, state: FSMContext):
    async with async_session() as session:

        data = await state.get_data()

        server = ServerList(
            password=message.text,
            user_id=message.from_user.id,
            ip=data.get('ip'),
        )

        session.add(server)
        await session.commit()
        await message.answer(SERVER_CREATED)
        logging.info('Server created')

    await state.clear()


@router.callback_query(F.data.startswith("server_"))
async def info_server(callback: CallbackQuery):

    server_id = int(callback.data.split("_")[1])

    async with async_session() as session:
        filter_result = await session.execute(
            select(ServerList).filter_by(id=server_id)
        )

        server = filter_result.scalar_one_or_none()

        if not server:
            return await callback.answer(NOT_SERVER, show_alert=True)

    await callback.message.answer(f"Check server: {server.ip}")
    await callback.message.answer(await result_check_server(server=server))

    return await callback.answer()