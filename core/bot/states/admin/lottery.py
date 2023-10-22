from aiogram.fsm.state import State, StatesGroup


class CreateLottery(StatesGroup):
    price = State()
    win = State()