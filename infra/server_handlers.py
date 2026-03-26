import logging

from aiogram import F, Router, html, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select

from engine_sql.db import async_session
from engine_sql.fsm_states import AddServer
from engine_sql.models import ServerList, User

from .ansible_check_server import check_server
from .validate import ValidateIP

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    async with async_session() as session:

        filter_result = await session.execute(
            select(User).filter_by(user_id=message.from_user.id)
        )

        user = filter_result.scalar_one_or_none()

        if not user:
            new_user = User(user_id=message.from_user.id)
            session.add(new_user)
            await session.commit()
            logging.info(f'User {message.from_user.full_name} added')
        else:
            logging.info('User in base')

    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}! \n"
                         f"Send >>> /servers")


@router.message(F.text.lower() == 'add server')
async def add_server_start(message: types.Message, state: FSMContext):
    await message.answer('Enter the server IP')
    await state.set_state(AddServer.waiting_for_ip)


@router.message(AddServer.waiting_for_ip)
async def process_ip(message: types.Message, state: FSMContext):
    async with async_session() as session:
        server_ip = message.text.strip()
        filter_result = await session.execute(select(ServerList).filter_by(
            ip=server_ip, user_id=message.from_user.id)
        )

        server = filter_result.scalar_one_or_none()

        if not server:
            validate_ip = ValidateIP(server_ip)
            if validate_ip.validate():
                await state.update_data(ip=server_ip)
                await message.answer('Send password for ip')
                await state.set_state(AddServer.waiting_for_password)
            else:
                await message.answer(
                    'The IP address is incorrect, '
                    'please send the correct address'
                )

        else:
            logging.info('Server in db')
            await message.answer('The server is on your list')


@router.message(AddServer.waiting_for_password)
async def process_password(message: types.Message, state: FSMContext):
    async with async_session() as session:

        data = await state.get_data()

        server = ServerList(
            password=message.text,
            user_id=message.from_user.id,
            ip=data['ip'], name='server'
        )

        session.add(server)
        await session.commit()
        await message.answer('New server created in db')
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
            return await callback.answer("Server not found", show_alert=True)

    await callback.message.answer(f"Check server: {server.ip}")
    runner = await check_server(server)
    result_check_server = {}
    for event in runner.events:
        if event.get('event') == 'runner_on_ok':
            task_name = event['event_data']['task']
            res = event['event_data']['res']

            if task_name == 'ping test':
                result_check_server['ping'] = res['ping']

            elif task_name == 'uptime server':
                result_check_server['uptime'] = res['stdout']
    await callback.message.answer(f"✅ {server.ip} \n\n"
                                  f"Ping: {result_check_server['ping']} \n"
                                  f"Uptime: {result_check_server['uptime']}"
                                  if runner.rc == 0 else "Error")

    return await callback.answer()

