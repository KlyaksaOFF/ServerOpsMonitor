import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

TOKEN = ""


dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")

@dp.message(Command('servers'))
async def cmd_hi(message: types.Message):
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
async def add_server(message: types.Message):
    await message.answer('Проверяем')

@dp.message(F.text.lower() == 'list connected servers')
async def list_connected_servers(message: types.Message):
    await message.reply('d')

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())