from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
import asyncio
from core.config import get_config
from core.bot.handlers.user.start import start_handler
from core.bot.handlers.user.registration import start_registration, get_name, get_position
from core.bot.states.user.registration import Registration
import logging

async def start():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    bot = Bot(token=get_config(".env").BOT_TOKEN)
    dp = Dispatcher()

    dp.message.register(start_handler, Command("start"))

    # User
    dp.message.register(start_registration, F.text == "Зарегистрироваться")
    dp.message.register(get_name, Registration.name)
    dp.message.register(get_position, Registration.position)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(start())