import asyncio
import logging
import sys
from dotenv import load_dotenv
from os import getenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from files.main_logic import router as router_main
from files.keyboard import router as router_keyboard

load_dotenv()
TOKEN = (getenv("BOT_TOKEN"))

dp = Dispatcher()
dp.include_router(router_main)
dp.include_router(router_keyboard)

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
