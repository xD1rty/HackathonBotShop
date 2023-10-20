from aiogram.fsm.state import State, StatesGroup

class Registration(StatesGroup):
    name = State()
    position = State()
