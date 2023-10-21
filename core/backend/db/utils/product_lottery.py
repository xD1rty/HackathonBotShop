from core.backend.db.models.lottery import ProductLottery
from core.backend.db.utils.product import get_product_by_id
from core.backend.db.utils.user import get_user_by_id
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from random import choice


async def create_product_lottery(product_id: int, price: int, session: AsyncSession):
    product = await get_product_by_id(product_id, session)
    if product:
        new_product_lottery = ProductLottery(price=price, product=product)
        session.add(new_product_lottery)
        await session.commit()
        return new_product_lottery
    raise Exception('нет продукта с таким id')


async def get_product_lottery_by_id(lottery_id: int, session: AsyncSession):
    return (await session.execute(select(ProductLottery).filter(ProductLottery.id == lottery_id))).scalar_one_or_none()


async def get_product_lottery_by_id_with_product(lottery_id: int, session: AsyncSession):
    return (await session.execute(select(ProductLottery)
                                  .filter(ProductLottery.id == lottery_id)
                                  .options(selectinload(ProductLottery.product)))
            ).scalar_one_or_none()


async def delete_product_lottery(lottery_id: int, session: AsyncSession):
    product_lottery = await get_product_lottery_by_id(lottery_id, session)
    await session.delete(product_lottery)
    await session.commit()
    return True


async def get_users_of_product_lottery_by_id(lottery_id: int, session: AsyncSession):
    product_lottery = await get_product_lottery_by_id(lottery_id, session)
    return product_lottery.users


async def add_user_to_product_lottery(tg_id: int, lottery_id: int, session: AsyncSession):
    user = await get_user_by_id(tg_id, session)
    product_lottery = await get_product_lottery_by_id_with_product(lottery_id, session)
    if user in product_lottery.users:
        raise Exception('вы уже учавствуете в лотерее')
    if user.balance >= product_lottery.price:
        user.balance -= product_lottery.price
        product_lottery.balance += product_lottery.price
        product_lottery.users.append(user)
        await session.commit()
        if product_lottery.balance >= product_lottery.product.price:
            winner = choice(product_lottery.users)
            return winner.id
        return True
    raise Exception('недостаточно денег на балансе')
