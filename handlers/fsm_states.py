from aiogram.fsm.state import State, StatesGroup


class AddServer(StatesGroup):
    waiting_for_ip = State()
    waiting_for_password = State()