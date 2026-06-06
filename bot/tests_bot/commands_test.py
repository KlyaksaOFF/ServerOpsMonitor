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
    session = getenv("STRING_SESSION").strip()
    client = TelegramClient(
        StringSession(session),
        api_id,
        api_hash)

    await client.connect()
    if not await client.is_user_authorized():
        await client.disconnect()
        raise RuntimeError("StringSession is not authorized")
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


@pytest.mark.asyncio(loop_scope="session")
async def test_list_servers(telegram_client):
    bot_login = (getenv("BOT_LOGIN"))

    async with telegram_client.conversation(bot_login) as conv:
        await conv.send_message('List connected servers')
        response = await conv.get_response()
        assert response is not None
        assert response.text == "You don't have servers"


@pytest.mark.asyncio(loop_scope="session")
async def test_add_server(telegram_client):
    bot_login = (getenv("BOT_LOGIN"))

    async with telegram_client.conversation(bot_login) as conv:
        await conv.send_message('Add server')
        response = await conv.get_response()
        assert response is not None
        assert response.text == "Enter the server IP"

        await conv.send_message('192.168.1.1')
        response = await conv.get_response()
        assert response is not None
        assert response.text == "Send password for ip"

        await conv.send_message('123456')
        response = await conv.get_response()
        assert response is not None
        assert response.text == "New server created in your list"

        await conv.send_message('List connected servers')
        response = await conv.get_response()
        assert response is not None
        if response.buttons:
            await response.click(3)