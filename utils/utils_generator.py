import asyncio

from telethon.sessions import StringSession
from telethon.sync import TelegramClient

API_ID = id  # your id
API_HASH = 'hash'  # your hash


async def generator():
    async with TelegramClient(StringSession(), API_ID, API_HASH) as client:
        print("\nYour string session (Строка сессии):\n")

        session_string = client.session.save()
        print(session_string)
        print("\nCopy the line above and save it in a safe place!")


if __name__ == '__main__':
    asyncio.run(generator())
