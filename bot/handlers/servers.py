from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.orm.exc import UnmappedInstanceError

from bot.handlers.fsm_states import AddServer
from services.server_check import (
    result_check_server,
)
from services.server_update import (
    result_update_server,
)
from texts.texts import (
    ENTER_IP,
    NOT_SERVER,
    SERVER_CREATED,
)
from utils.utils_servers_bot import ResponseBotServers

router = Router()


@router.message(Command('start'))
async def start(message: types.Message):
    await message.answer('Enter the command /servers and '
                         'click on the button you need.')


@router.message(F.text.lower() == 'add server')
async def add_server_start(message: types.Message, state: FSMContext):
    await message.answer(ENTER_IP)
    await state.set_state(AddServer.waiting_for_ip)


@router.message(AddServer.waiting_for_ip)
async def process_ip(message: types.Message, state: FSMContext):
    server_ip = message.text.strip()
    user_id = message.from_user.id
    response = ResponseBotServers(ip=server_ip, user_id=user_id)

    await response.process_ip(state=state, message=message)


@router.message(AddServer.waiting_for_password)
async def process_password(message: types.Message, state: FSMContext):
    data = await state.get_data()
    response = ResponseBotServers(
        ip=data.get('ip'),
        user_id=message.from_user.id,
        password=message.text)

    await response.process_password()
    await message.answer(SERVER_CREATED)
    await state.clear()


@router.callback_query(F.data.startswith("server_"))
async def ip_server(callback: CallbackQuery):
    server_id = int(callback.data.split("_")[1])
    response = ResponseBotServers(server_id=server_id)
    server = await response.get_server()

    if not server:
        return await callback.answer(NOT_SERVER, show_alert=True)

    return await callback.answer(server.ip)


@router.callback_query(F.data.startswith("check_"))
async def info_server(callback: CallbackQuery):

    server_id = int(callback.data.split("_")[1])
    response = ResponseBotServers(server_id=server_id)
    server = await response.get_server()

    if not server:
        return await callback.answer(NOT_SERVER, show_alert=True)

    await callback.message.answer(f"Check server: {server.ip}")
    await callback.message.answer(await result_check_server(server=server))

    return await callback.answer()


@router.callback_query(F.data.startswith("remove_"))
async def remove_server(callback: CallbackQuery):
    try:
        server_id = int(callback.data.split("_")[1])
        response = ResponseBotServers(server_id=server_id)
        await response.remove_server()
        await callback.message.answer('Server removed')

    except UnmappedInstanceError:
        await callback.message.answer('The server has already been deleted')

    return await callback.answer()


@router.callback_query(F.data.startswith("update_"))
async def update_server(callback: CallbackQuery):
    server_id = int(callback.data.split("_")[1])

    response = ResponseBotServers(server_id=server_id)
    server = await response.get_server()

    if not server:
        return await callback.answer(NOT_SERVER, show_alert=True)
    await callback.message.answer("""
    Warning! The update may take 
    anywhere from a few seconds to more than 5 minutes.
    During this time, you can continue using the bot 
    and checking the servers, as my bot is asynchronous.
    """)

    return await callback.message.answer(
        await result_update_server(server=server)
    )


@router.callback_query(F.data.startswith("autocheck_"))
async def authcheck_function(callback: CallbackQuery):
    server_id = int(callback.data.split("_")[1])
    response = ResponseBotServers(server_id=server_id)
    server = await response.get_server()

    if not server:
        return await callback.answer(NOT_SERVER, show_alert=True)

    await response.autocheck_process()

    state_server = await response.autocheck_state()
    return await callback.message.answer(state_server)