from aiogram.fsm.state import State, StatesGroup

class CreateCategory(StatesGroup):
    name = State()