import asyncio
import logging
import sys
from dotenv import load_dotenv
from os import getenv
from sqlalchemy import select
from aiogram import Bot, Dispatcher, html, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from engine_sql.models import User, ServerList, async_session, AddServer
from aiogram.fsm.context import FSMContext
from ansible_runner import run_async

load_dotenv()
TOKEN = (getenv("BOT_TOKEN"))

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    async with async_session() as session:
        result = await session.execute(select(User).filter_by(user_id=message.from_user.id))
        user = result.scalar_one_or_none()
        if not user:
            new_user = User(user_id=message.from_user.id)
            session.add(new_user)
            await session.commit()
            print(f'User {message.from_user.full_name} added!')
        else:
            print(f'User in base!')

    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")

@dp.message(Command('servers'))
async def cmd_servers(message: types.Message):
    buttons = [
        [
            types.KeyboardButton(text='Add server'),
            types.KeyboardButton(text='List connected servers')
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder='Press the button'
    )
    await message.answer(f'Press the button', reply_markup=keyboard)


@dp.message(F.text.lower() == 'add server')
async def add_server_start(message: types.Message, state: FSMContext):
    await message.answer('Enter the server IP')
    await state.set_state(AddServer.waiting_for_ip)

@dp.message(AddServer.waiting_for_ip)
async def process_ip(message: types.Message, state: FSMContext):
    async with async_session() as session:
        result = await session.execute(select(ServerList).filter_by(ip=message.text))
        server = result.scalar_one_or_none()
        if not server:
            await state.update_data(ip=message.text)
            await message.answer(f'Send password for ip')
            await state.set_state(AddServer.waiting_for_password)
        else:
            print('Server in db')
            await message.answer(f'Server have in db')

@dp.message(AddServer.waiting_for_password)
async def process_password(message: types.Message, state: FSMContext):
    async with async_session() as session:
            data = await state.get_data()
            server = ServerList(password=message.text, user_id=message.from_user.id, ip=data['ip'], name='server')
            session.add(server)
            await session.commit()
            await message.answer('New server created in db')
    await state.clear()

@dp.message(F.text.lower() == 'list connected servers')
async def list_connected_servers(message: types.Message):
    async with async_session() as session:
        result = await session.execute(select(ServerList).filter_by(user_id=message.from_user.id))
        servers = result.scalars().all()
        if not servers:
            return await message.answer("You don't have servers")

        response_text = "<b>List your servers:</b>\n\n"

        for i, server in enumerate(servers, start=1):
            response_text += f"{i}. ID: <code>{server.id}</code> | IP: {server.ip}\n"
        await message.answer(response_text, parse_mode="HTML")


@dp.message(F.text.lower() == '202.181.188.233')
async def test_server(message: types.Message):

    target_ip = '202.181.188.233'

    thread, runner = run_async(
        inventory=f"{target_ip}",
        extravars={'ansible_user': 'root'},
        playbook=[{'hosts': 'all', 'gather_facts': 'no', 'tasks': [{'ping': None}]}]
    )

    while thread.is_alive():
        await asyncio.sleep(0.1)

    if runner.rc == 0:
        await message.answer(f"✅ {target_ip} доступен!")
    else:
        await message.answer(f"❌ Ошибка подключения")

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
