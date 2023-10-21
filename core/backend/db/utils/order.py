from core.backend.db.models.order import Order
from core.backend.db.utils.product import get_product_by_id
from core.backend.db.utils.user import get_user_by_id
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def add_order(tg_id: int, product_id: int, session: AsyncSession):
    user = await get_user_by_id(tg_id, session)
    product = await get_product_by_id(product_id, session)
    order = Order(user=user, product=product)
    session.add(order)
    await session.commit()


async def get_order_by_id(order_id: int, session: AsyncSession):
    return (await session.execute(select(Order).filter(Order.id == order_id))).scalar_one_or_none()


async def change_status_by_id(order_id: int, status: bool, session: AsyncSession):
    order = await get_order_by_id(order_id, session)
    order.status = status
    await session.commit()
    return True
