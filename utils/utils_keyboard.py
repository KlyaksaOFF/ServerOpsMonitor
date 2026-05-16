from aiogram import types

from repositories.server_repository import (
    list_user_connected_servers,
    state_autocheck_server,
)


class data_keyboard:
    def __init__(self, user_id=None):
        self.user_id = user_id

    async def servers(self):
        servers = await list_user_connected_servers(self.user_id)
        return servers

    @staticmethod
    async def result_keyboard(servers):
        buttons = []

        for server in servers:
            buttons.append(
                [
                types.InlineKeyboardButton(
                    text=server.ip,
                    callback_data=f'server_{server.id}'),

                types.InlineKeyboardButton(
                    text='check',
                    callback_data=f'check_{server.id}'),

                types.InlineKeyboardButton(
                    text='update',
                    callback_data=f'update_{server.id}'),

                types.InlineKeyboardButton(
                    text='remove',
                    callback_data=f'remove_{server.id}'),

                types.InlineKeyboardButton(
                    text=await state_autocheck_server(server.id),
                    callback_data=f'autocheck_{server.id}')
                ])
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard