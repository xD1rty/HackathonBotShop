from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

reg_button = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Зарегистрироваться 📝")
    ]
])

user_menu = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Магазин 🛒"),
        KeyboardButton(text="Профиль 👤")
    ],
    [
        KeyboardButton(text="Создать чек 📃"),
        KeyboardButton(text="Ставка")
    ]
])

admin_menu = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Список юзеров бота 📋"),
        KeyboardButton(text="Начислить баланс 💵")
    ],
    [
        KeyboardButton(text="Создать категорию 🏷"),
        KeyboardButton(text="Создать товар 📦")
    ],
    [
        KeyboardButton(text="Создать розыгрыш денег"),
        KeyboardButton(text="Создать розыгрыш вещей")
    ]
])