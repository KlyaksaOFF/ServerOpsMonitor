from .check_server import ping_server
import logging
from sqlalchemy import select
from aiogram import html, types, F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from engine_sql.models import User, ServerList, async_session, AddServer
from aiogram.fsm.context import FSMContext
from .validate import ValidateIP

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    async with async_session() as session:

        result = await session.execute(select(User).filter_by(user_id=message.from_user.id))
        user = result.scalar_one_or_none()

        if not user:
            new_user = User(user_id=message.from_user.id)
            session.add(new_user)
            await session.commit()
            logging.info(f'User {message.from_user.full_name} added!')
        else:
            logging.info(f'User in base!')

    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@router.message(F.text.lower() == 'add server')
async def add_server_start(message: types.Message, state: FSMContext):
    await message.answer('Enter the server IP')
    await state.set_state(AddServer.waiting_for_ip)


@router.message(AddServer.waiting_for_ip)
async def process_ip(message: types.Message, state: FSMContext):
    async with async_session() as session:

        result = await session.execute(select(ServerList).filter_by(ip=message.text, user_id=message.from_user.id))
        server = result.scalar_one_or_none()

        if not server:
            validate_ip = ValidateIP(message.text)
            if validate_ip.validate():
                await state.update_data(ip=message.text)
                await message.answer(f'Send password for ip')
                await state.set_state(AddServer.waiting_for_password)
            else:
                await message.answer('The IP address is incorrect, please send the correct address')
        else:
            logging.info('Server in db')
            await message.answer(f'The server is on your list')


@router.message(AddServer.waiting_for_password)
async def process_password(message: types.Message, state: FSMContext):
    async with async_session() as session:

            data = await state.get_data()
            server = ServerList(password=message.text, user_id=message.from_user.id, ip=data['ip'], name='server')
            session.add(server)
            await session.commit()
            await message.answer('New server created in db')
            logging.info('Server created')

    await state.clear()


@router.callback_query(F.data.startswith("server_"))
async def info_server(callback: CallbackQuery):

    server_id = int(callback.data.split("_")[1])

    async with async_session() as session:
        result = await session.execute(select(ServerList).filter_by(id=server_id))
        server = result.scalar_one_or_none()

        if not server:
            return await callback.message.answer("Server not found", show_alert=True)

    await callback.message.answer(f"{server.id}. {server.ip}, {server.user_id}, {server.password}")

    runner = await ping_server(server)

    if runner.rc == 0:
        await callback.message.answer(f"✅ {server.ip} success!")
    else:
        await callback.message.answer(f"❌ Error")
    await callback.answer()

