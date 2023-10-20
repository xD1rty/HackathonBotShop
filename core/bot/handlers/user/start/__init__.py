from aiogram import Bot, types, filters
from core.text import start_non_user, start_admin, admin_user_request
from core.bot.keyboards.reply import reg_button
from core.config import get_config

async def start_handler(
        message: types.Message,
        bot: Bot,
        command: filters.CommandObject):
    if command.args:
        pass
    else:
        if message.from_user.id == get_config(".env").ADMIN_ID:
            await message.answer(start_admin.format(name=message.from_user.first_name))
        else:
            await message.answer(start_non_user, reply_markup=reg_button)