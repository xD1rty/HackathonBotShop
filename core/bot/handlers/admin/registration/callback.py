from aiogram import Bot
from aiogram.types import CallbackQuery
from core.text import reg_ban, reg_accept, admin_user_request_accept, admin_user_request_ban
from core.bot.keyboards.reply import user_menu
from core.backend.db.utils.user import edit_status, get_user
from sqlalchemy.ext.asyncio import AsyncSession

async def ban_or_accept_user(call: CallbackQuery, bot: Bot, session: AsyncSession):
    if "ban_" in call.data:
        telegram_user_id = int(call.data.replace("ban_", "").strip())
        await bot.send_message(telegram_user_id, reg_ban)
        await call.message.answer(admin_user_request_ban.format(id=telegram_user_id))
        await edit_status(telegram_user_id, False, session)
        await call.answer()
    if "accept_" in call.data:
        telegram_user_id = int(call.data.replace("accept_", "").strip())
        user = await get_user(telegram_user_id, session)
        await bot.send_message(telegram_user_id, reg_accept.format(
            name=user.name,
            balance = user.balance,
            id = telegram_user_id
        ), reply_markup=user_menu)
        await edit_status(telegram_user_id, True, session)
        await call.message.answer(admin_user_request_accept.format(name=user.name, position=user.position, id=telegram_user_id, telegram_tag=user.telegram_tag))
        await call.answer()