from aiogram.fsm.state import StatesGroup, State


class AddServer(StatesGroup):
    waiting_for_ip = State()
    waiting_for_password = State()