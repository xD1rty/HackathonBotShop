from core.backend.db.models.lottery import MoneyLottery
from core.backend.db.utils.user import get_user_by_id
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from random import choice


async def create_money_lottery(price: int, money_prize: int, session: AsyncSession):
    new_money_lottery = MoneyLottery(price=price, money_prize=money_prize)
    session.add(new_money_lottery)
    await session.commit()
    return new_money_lottery


async def get_money_lottery_by_id(lottery_id: int, session: AsyncSession):
    return (await session.execute(select(MoneyLottery).filter(MoneyLottery.id == lottery_id))).scalar_one_or_none()


async def get_money_lottery_by_id_with_user(lottery_id: int, session: AsyncSession):
    return (await session.execute(select(MoneyLottery).filter(MoneyLottery.id == lottery_id).options(selectinload(MoneyLottery.users)))).scalar_one_or_none()


async def delete_money_lottery(lottery_id: int, session: AsyncSession):
    money_lottery = await get_money_lottery_by_id(lottery_id, session)
    await session.delete(money_lottery)
    await session.commit()
    return True


async def get_users_of_money_lottery_by_id(lottery_id: int, session: AsyncSession):
    money_lottery = await get_money_lottery_by_id(lottery_id, session)
    return money_lottery.users


async def add_user_to_money_lottery(tg_id: int, lottery_id: int, session: AsyncSession):
    user = await get_user_by_id(tg_id, session)
    money_lottery = await get_money_lottery_by_id_with_user(lottery_id, session)
    if user in money_lottery.users:
        raise Exception('вы уже учавствуете в лотерее')
    if user.balance >= money_lottery.price:
        user.balance -= money_lottery.price
        money_lottery.balance += money_lottery.price
        money_lottery.users.append(user)
        await session.commit()
        if money_lottery.balance >= money_lottery.money_prize:
            await delete_money_lottery(lottery_id, session)
            winner = choice(money_lottery.users)
            return winner.id
        return True
    raise Exception('недостаточно денег на балансе')
