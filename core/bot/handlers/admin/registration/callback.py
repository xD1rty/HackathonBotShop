from aiogram import Bot
from aiogram.types import CallbackQuery


async def ban_or_accept_user(call: CallbackQuery, bot: Bot):
    if "ban_" in call.data:
        telegram_user_id = int(call.data.replace("ban_", "").strip())
        await bot.send_message(telegram_user_id, "К сожалению, тебя не взяли(")
        await call.message.answer("Все")
        await call.answer()
    if "accept_" in call.data:
        telegram_user_id = int(call.data.replace("accept_", "").strip())
        await bot.send_message(telegram_user_id, "Приветствуем в рядах компании)")
        await call.message.answer("FF")
        await call.answer()