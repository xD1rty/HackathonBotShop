from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from core.backend.db.utils.user import add_money, remove_money
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types.dice import DiceEmoji
from core.bot.states.user.stavki import Stavki


async def start_stavki(
        message: Message,
        state: FSMContext
):
    await message.answer("Введите, сколько монет вы ставите:")
    await state.set_state(Stavki.money)

async def stavki_money(
        message: Message,
        state: FSMContext,
):
    try:
        await state.update_data(money=int(message.text))
        await message.answer("Введите, сколько выпадет?")
        await state.set_state(Stavki.value)
    except:
        await message.answer("Введите число!!!")


async def stavki_value(
        message: Message,
        bot: Bot,
        state: FSMContext,
        session: AsyncSession
):
    try:
        data = await state.get_data()
        value = int(message.text)
        await remove_money(message.from_user.id, data["money"], session)
        result = await bot.send_dice(message.from_user.id, emoji=DiceEmoji.DICE)
        print(result)
        if result.dice.value == value:
            await add_money(message.from_user.id, data["money"]*2, session)
            await message.answer("Вы выиграли!!!")
        else:
            await message.answer("Вы проиграли")

    except TypeError:
        await message.answer("Введите корректное значение!!!")