from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
import asyncio
from aiogram.enums.parse_mode import ParseMode
from core.config import get_config
from core.bot.handlers.user.start import start_handler
from core.bot.handlers.user.registration import start_registration, get_name, get_position
from core.bot.states.user.registration import Registration
from core.bot.handlers.admin.registration.callback import ban_or_accept_user
from core.bot.middlewares.db import DbSessionMiddleware
from core.backend.db.db_setup import init_db, session
from core.bot.handlers.user.profile import get_profile
from core.bot.states.admin.money import MoneyAdd
from core.bot.handlers.admin.menu import add_user_money, set_money, get_money_count, get_all_users_handler
from core.bot.handlers.user.money_send import create_money_token, create_money_token_final
from core.bot.states.user.money_send import SendMoney
from core.bot.handlers.admin.menu.category_and_product import create_category, get_name_category, create_product, create_product_photos, create_product_category, create_product_name, create_product_desc, create_product_price
from core.bot.states.admin.category import CreateCategory
from core.bot.states.admin.product import CreateProduct
from core.bot.states.user.shopping import GetProductsByCategory
from core.bot.handlers.user.shopping import get_product_by_category_start, get_all_products_by_category

import logging

async def start():
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    bot = Bot(token=get_config(".env").BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    dp.update.middleware(DbSessionMiddleware(session_pool=session))

    dp.startup.register(init_db)

    dp.message.register(start_handler, Command("start"))

    # User
    dp.message.register(start_registration, F.text == "Зарегистрироваться")
    dp.message.register(get_name, Registration.name)
    dp.message.register(get_position, Registration.position)
    dp.message.register(get_profile, F.text == "Профиль")
    dp.message.register(create_money_token, F.text == "Создать чек")
    dp.message.register(create_money_token_final, SendMoney.money)
    dp.message.register(get_product_by_category_start, F.text == "Магазин")
    dp.message.register(get_all_products_by_category, GetProductsByCategory.category)
    dp.callback_query.register(ban_or_accept_user)

    # Admin

    dp.message.register(add_user_money, F.text == "Начислить баланс")
    dp.message.register(get_money_count, MoneyAdd.id)
    dp.message.register(set_money, MoneyAdd.money)
    dp.message.register(get_all_users_handler, F.text == "Список юзеров бота")
    dp.message.register(create_category, F.text == "Создать категорию")
    dp.message.register(get_name_category, CreateCategory.name)
    dp.message.register(create_product, F.text == "Создать товар")
    dp.message.register(create_product_name, CreateProduct.title)
    dp.message.register(create_product_desc, CreateProduct.description)
    dp.message.register(create_product_price, CreateProduct.price)
    dp.message.register(create_product_category, CreateProduct.category)
    dp.message.register(create_product_photos, CreateProduct.photos)

    try:
        await dp.start_polling(bot)
    except Exception as exc:
        logging.error(type(exc), exc, exc.__traceback__)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(start())