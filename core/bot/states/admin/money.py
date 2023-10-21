from aiogram.fsm.state import State, StatesGroup

class MoneyAdd(StatesGroup):
    id = State()
    money = State()