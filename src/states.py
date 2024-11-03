from aiogram.fsm.state import StatesGroup, State


class RequestForm(StatesGroup):
    username = State()
    subdomain = State()
