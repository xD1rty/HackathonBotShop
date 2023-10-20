from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def create_keyboard_accept_user(id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Запретить", callback_data=f"ban_{id}"),
            InlineKeyboardButton(text="Разрешить", callback_data=f"accept_{id}")
        ]
    ])