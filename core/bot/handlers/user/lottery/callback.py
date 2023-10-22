from aiogram.types import CallbackQuery
from core.backend.db.utils.money_lottery import get_money_lottery_by_id, add_user_to_money_lottery
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import Bot
from core.backend.db.utils.user import add_money

async def add_user_to_lottery_money(
        call: CallbackQuery,
        session: AsyncSession,
        bot: Bot
):
    try:
        user_id = call.from_user.id
        lottery_id = int(call.data.replace("moneyl_", "").strip())
        lottery = await get_money_lottery_by_id(lottery_id, session)
        result = await add_user_to_money_lottery(user_id, lottery_id, session)
        if result == True:
            await call.message.answer("Отлично! Вы учавствуете!")
        else:
            for user in lottery.users:
                if user.id != result:
                    await bot.send_message(user.id, "Вы не выиграли в розыгрыше(((")
                else:
                    await bot.send_message(result, "Ты выиграл в розыгрыше!! Поздравляю")
                    await add_money(result, lottery.money_prize, session)
    except Exception: await call.message.answer("Либо ты уже участвуешь, либо нет денег, либо розыгрыш удален")