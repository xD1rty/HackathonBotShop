from aiogram.fsm.state import State, StatesGroup


class GetProductsByCategory(StatesGroup):
    category = State()