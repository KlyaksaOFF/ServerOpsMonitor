import logging

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.fsm_states import AddServer
from repositories.server_repository import (
    create_server,
    get_server_by_id,
    process_add_server,
)
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

router = Router()


@router.message(F.text.lower() == 'add server')
async def add_server_start(message: types.Message, state: FSMContext):
    await message.answer(ENTER_IP)
    await state.set_state(AddServer.waiting_for_ip)


@router.message(AddServer.waiting_for_ip)
async def process_ip(message: types.Message, state: FSMContext):
    server_ip = message.text.strip()
    user_id = message.from_user.id

    result = await process_add_server(
        server_ip=server_ip,
        user_id=user_id,
        state=state
    )
    if result == "valid_ip":
        await message.answer(SEND_PASSWORD)
    elif result == "invalid_ip":
        await message.answer(ERROR_INVALID_IP)
    else:
        await message.answer(SERVER_IN_YOUR_LIST)


@router.message(AddServer.waiting_for_password)
async def process_password(message: types.Message, state: FSMContext):
    await create_server(state=state,
                        user_id=message.from_user.id,
                        password=message.text)
    await message.answer(SERVER_CREATED)
    logging.info('Server created')

    await state.clear()


@router.callback_query(F.data.startswith("server_"))
async def info_server(callback: CallbackQuery):

    server_id = int(callback.data.split("_")[1])

    server = await get_server_by_id(server_id)

    if not server:
        return await callback.answer(NOT_SERVER, show_alert=True)

    await callback.message.answer(f"Check server: {server.ip}")
    await callback.message.answer(await result_check_server(server=server))

    return await callback.answer()