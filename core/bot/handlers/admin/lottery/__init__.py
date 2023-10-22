from core.backend.db.utils.money_lottery import create_money_lottery, get_money_lottery_by_id
from aiogram import Bot
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from core.backend.db.utils.user import get_all_users
from core.bot.states.admin.lottery import CreateLottery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from core.config import get_config



async def create_lottery_start(
        message: Message,
        bot: Bot,
        state: FSMContext,
        session: AsyncSession
):

    await message.answer("Введите, сколько стоит участие в лотерее")
    await state.set_state(CreateLottery.price)


async def create_lottery_price(
        message: Message,
        bot: Bot,
        state: FSMContext,
        session: AsyncSession
):
    try:
        await state.update_data(price=int(message.text))
        await message.answer("Введите выигрыш в лотерее!")
        await state.set_state(CreateLottery.win)
    except TypeError:
        await message.answer("Введите валидное значение!!!!")


async def create_lottery_win(
        message: Message,
        bot: Bot,
        state: FSMContext,
        session: AsyncSession
):
    try:
        win = int(message.text)
        data = await state.get_data()
        await state.clear()
        lottery = await create_money_lottery(data["price"], win, session)
        users = await get_all_users(session)
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="✅ Участвую", callback_data=f"moneyl_{lottery.id}")
                ]
            ]
        )
        for user in users:
            await bot.send_message(chat_id=user.id, text=f"Здравствуй! Тут начался розыгрыш (денег)!\nСтоимость участия: {lottery.price}\nПриз: {lottery.money_prize}", reply_markup=keyboard)

        await message.answer("Розыгрыш на деньги создан!")

    except TypeError:
        await message.answer("Введите корректное значение!")