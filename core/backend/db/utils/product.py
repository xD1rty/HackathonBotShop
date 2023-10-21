from core.backend.db.models.product import Product
from core.backend.db.utils.category import get_category_by_title
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from aiogram.types import Message
from typing import List
from io import BytesIO


async def add_product(message_type: str, title: str, description: str, price: int, category_title: str,
                      session: AsyncSession, photo: str):
    category = await get_category_by_title(category_title, session)
    if category:
        new_product = Product(message_type=message_type, title=title, description=description, price=price,
                              photo=photo, category=category)
        session.add(new_product)
        await session.commit()
        return new_product
    raise Exception('нет такой категории')


async def get_product_by_id(product_id: int, session: AsyncSession):
    return (await session.execute(select(Product).filter(Product.id == product_id))).scalar_one_or_none()
