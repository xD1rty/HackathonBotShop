from aiogram.fsm.state import State, StatesGroup


class SendMoney(StatesGroup):
    money = State()
