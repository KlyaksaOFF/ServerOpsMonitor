from sqlalchemy import select
from aiogram import types, F, Router
from aiogram.filters import Command
from engine_sql.models import ServerList, async_session
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(F.text.lower() == 'list connected servers')
async def connected_servers(message: types.Message):
    async with async_session() as session:

        filter_result = await session.execute(select(ServerList).filter_by(user_id=message.from_user.id))
        servers = filter_result.scalars().all()

        if not servers:
            return await message.answer("You don't have servers")

        buttons = []

        for server in servers:
            buttons.append([types.InlineKeyboardButton(text=server.ip, callback_data=f'server_{server.id}')])
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

        return await message.answer("Select server", reply_markup=keyboard)


@router.message(Command('servers'))
async def menu_servers(message: types.Message, state: FSMContext):
    await state.clear()
    buttons = [[types.KeyboardButton(text='Add server'),
    types.KeyboardButton(text='List connected servers')],]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder='Press the button'
    )

    return await message.answer(f'Press the button', reply_markup=keyboard)