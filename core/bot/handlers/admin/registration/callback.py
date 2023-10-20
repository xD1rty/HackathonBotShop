from aiogram import Bot
from aiogram.types import CallbackQuery
from core.text import reg_ban, reg_accept, admin_user_request_accept, admin_user_request_ban

async def ban_or_accept_user(call: CallbackQuery, bot: Bot):
    if "ban_" in call.data:
        telegram_user_id = int(call.data.replace("ban_", "").strip())
        await bot.send_message(telegram_user_id, reg_ban)
        await call.message.answer(admin_user_request_ban.format(id=telegram_user_id))
        await call.answer()
    if "accept_" in call.data:
        telegram_user_id = int(call.data.replace("accept_", "").strip())
        await bot.send_message(telegram_user_id, reg_accept.format(
            name="ПОка нет БД",
            balance = "10000",
            id = telegram_user_id
        ))
        await call.message.answer(admin_user_request_accept.format(name="нет бд", position="нет бд", id=telegram_user_id, telegram_tag="pip пока нет"))
        await call.answer()