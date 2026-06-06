import asyncio
import pathlib
from os import getenv

from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.sessions import StringSession

load_dotenv()


async def main():
    api_id = int(getenv("API_ID"))
    api_hash = getenv("API_HASH")
    project_root = pathlib.Path(__file__).resolve().parents[2]
    session_path = project_root / 'test_session'

    client = TelegramClient(str(session_path), api_id=api_id, api_hash=api_hash)
    string = StringSession.save(client.session)
    print(string)
    await client.start()
    print("Successfully authorized! "
    "Check if the file appears in the project root.")
    await client.disconnect()


if __name__ == '__main__':
    asyncio.run(main())
