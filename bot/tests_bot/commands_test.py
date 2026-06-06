from os import getenv

import pytest
import pytest_asyncio
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.sessions import StringSession

load_dotenv()


@pytest_asyncio.fixture(scope="session")
async def telegram_client():
    api_id = int(getenv("API_ID"))
    api_hash = getenv("API_HASH")
    session = getenv("STRING_SESSION")

    client = TelegramClient(
        StringSession(session),
        api_id,
        api_hash,
    )

    await client.connect()

    if not await client.is_user_authorized():
        await client.disconnect()
        raise RuntimeError("StringSession is not authorized")

    print(await client.get_me())

    yield client

    await client.disconnect()


@pytest.mark.asyncio(loop_scope="session")
async def test_start(telegram_client):
    bot_login = (getenv("BOT_LOGIN"))

    async with telegram_client.conversation(bot_login) as conv:
        await conv.send_message('/start')

        response = await conv.get_response()
        assert response is not None
        assert response.text == ("Enter the command "
        "/servers and click on the button you need.")