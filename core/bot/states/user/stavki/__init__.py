from aiogram.fsm.state import StatesGroup, State

class Stavki(StatesGroup):
    money = State()
    value = State()