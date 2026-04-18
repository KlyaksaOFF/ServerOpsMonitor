from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from repositories.server_repository import (
    list_user_connected_servers,
    state_autocheck_server,
)

router = Router()


@router.message(F.text.lower() == 'list connected servers')
async def connected_servers(message: types.Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    servers = await list_user_connected_servers(user_id)

    if not servers:
        return await message.answer("You don't have servers")

    buttons = []

    for server in servers:
        buttons.append([types.InlineKeyboardButton(
            text=server.ip, callback_data=f'server_{server.id}'
        ),
                        types.InlineKeyboardButton(
                            text='check', callback_data=f'check_{server.id}'),

        types.InlineKeyboardButton(text='update',
                                   callback_data=f'update_{server.id}'),

        types.InlineKeyboardButton(text='remove',
                                   callback_data=f'remove_{server.id}'),
        types.InlineKeyboardButton(text=await state_autocheck_server(server.id),
                                    callback_data=f'autocheck_{server.id}'),
        ]
        )
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    return await message.answer("Select server", reply_markup=keyboard)


@router.message(Command('servers'))
async def menu_servers(message: types.Message, state: FSMContext):
    await state.clear()
    buttons = [[types.KeyboardButton(text='Add server'),
    types.KeyboardButton(text='List connected servers')]]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder='Press the button'
    )

    return await message.answer('Press the button', reply_markup=keyboard)