from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

reg_button = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Зарегистрироваться")
    ]
])

user_menu = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Магазин"),
        KeyboardButton(text="Профиль")
    ],
    [
        KeyboardButton(text="Создать чек")
    ]
])