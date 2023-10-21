from aiogram import Bot
from aiogram.types import Message
from core.backend.db.utils.token import create_token
from sqlalchemy.ext.asyncio import (AsyncSession)
from core.bot.states.user.money_send import SendMoney
from aiogram.fsm.context import FSMContext


async def create_money_token(
        message: Message,
        bot: Bot,
        state: FSMContext,
        session: AsyncSession
):
    await message.answer("Введите кол-во монет, которое вы хотите отправить:")
    await state.set_state(SendMoney.money)

async def create_money_token_final(
        message: Message,
        bot: Bot,
        state: FSMContext,
        session: AsyncSession
):
    try:
        token = await create_token(message.from_user.id, int(message.text), session)
        await message.answer(f"Ваша ссылка на получение монет: \n\nt.me/intensa_shop_bot?start={token.token}")
        await state.clear()
    except TypeError:
        await message.answer("Попробуй снова, тут ошибка")
    except Exception:
        await message.answer("Недостаточно средств! Нажмите /start")
        await state.clear()