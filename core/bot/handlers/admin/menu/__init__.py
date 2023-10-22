from aiogram import Bot
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from core.backend.db.utils.user import add_money
from core.config import get_config
from core.bot.states.admin.money import MoneyAdd
from aiogram.fsm.context import FSMContext
from core.backend.db.utils.user import get_all_users


async def add_user_money(
        message: Message,
        state: FSMContext
):
    if message.from_user.id == get_config(".env").ADMIN_ID:
        await message.answer("Введите ID🪪 пользователя:")
        await state.set_state(MoneyAdd.id)
    else:
        await message.answer("Доступ запрещен!🚫")


async def get_money_count(
        message: Message,
        state: FSMContext
):
    if message.from_user.id == get_config(".env").ADMIN_ID:
        try:
            id = int(message.text)
            await state.update_data(id=id)
            await message.answer("Введите кол-во ИнтКоинов💵:")
            await state.set_state(MoneyAdd.money)
        except:
            await message.answer("Пробуй снова! Произошла ошибка😞")
    else:
        await message.answer("Доступ запрещен!🚫")


async def set_money(
        message: Message,
        bot: Bot,
        state: FSMContext,
        session: AsyncSession
):
    try:
        count = int(message.text)
        await state.update_data(count=count)
        data = await state.get_data()
        await state.clear()
        await add_money(data["id"], data["count"], session)
        await bot.send_message(data["id"], f"Администратор вам зачислил {data['count']} ТС!💵\nВводи /start🔧")
        await message.answer(f"Вы начислили {data['count']} TC на счет {data['id']}💸")
    except:
        await message.answer("Пробуй снова! Произошла ошибка😞")


async def get_all_users_handler(
        message: Message,
        session: AsyncSession
):
    text = """
Список всех юзеров бота📋\n\nИмя👤 / ID🪪 / Баланс💵 \n"""
    for i in await get_all_users(session):
        text+=f"{i.name} / <code>{i.id}</code> / <b>{i.balance} TC</b>\n"
    await message.answer(text)