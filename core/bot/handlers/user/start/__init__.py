from aiogram import Bot, types, filters
from core.text import start_non_user, start_admin, admin_user_request, reg_ban, reg_finish, start_user
from core.bot.keyboards.reply import reg_button
from sqlalchemy.ext.asyncio import AsyncSession
from core.config import get_config
from core.backend.db.utils.user import get_user
from core.bot.keyboards.reply import admin_menu

async def start_handler(
        message: types.Message,
        bot: Bot,
        command: filters.CommandObject,
        session: AsyncSession
):
    if command.args:
        pass
    else:
        if message.from_user.id == get_config(".env").ADMIN_ID:
            await message.answer(start_admin.format(name=message.from_user.first_name), reply_markup=admin_menu)
        else:
            user = await get_user(message.from_user.id, session)
            if user == None:
                await message.answer(start_non_user, reply_markup=reg_button)
            else:
                if user.is_worker == None:
                    await message.answer(reg_finish)
                elif user.is_worker == False:
                    await message.answer(reg_ban)
                else:
                    await message.answer(start_user.format(name=user.name, id=user.id, balance=user.balance))