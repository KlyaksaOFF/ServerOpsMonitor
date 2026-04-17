import asyncio

from repositories.server_repository import (
    get_all_servers,
)
from services.server_check import (
    result_check_server,
)


async def auto_check_servers(bot):
    while True:

        servers = await get_all_servers()

        for server in servers:
            result = await result_check_server(server)
            user_id = server.user_id
            await bot.send_message(chat_id=user_id, text=result)

        await asyncio.sleep(21600)