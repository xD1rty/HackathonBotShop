from aiogram.fsm.state import StatesGroup, State

class CreateProduct(StatesGroup):
    title = State()
    description = State()
    price = State()
    category = State()
    photos = State()