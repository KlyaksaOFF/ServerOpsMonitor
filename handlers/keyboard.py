from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from utils.utils_keyboard import DataKeyboard

router = Router()


@router.message(F.text.lower() == 'list connected servers')
async def connected_servers(message: types.Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    keyboard_process = DataKeyboard(user_id=user_id)
    servers = await keyboard_process.servers()

    if not servers:
        return await message.answer("You don't have servers")

    keyboard = await keyboard_process.result_keyboard(servers=servers)
    return await message.answer("Select server", reply_markup=keyboard)


@router.message(Command('servers'))
async def menu_servers(message: types.Message, state: FSMContext):
    await state.clear()
    buttons = [[types.KeyboardButton(text='Add server'),
    types.KeyboardButton(text='List connected servers')]]

    keyboard = types.ReplyKeyboardMarkup(
    keyboard=buttons,
    resize_keyboard=True,
    input_field_placeholder='Press the button')
    return await message.answer('Press the button', reply_markup=keyboard)