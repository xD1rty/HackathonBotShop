from core.backend.db.models.product import Product
from core.backend.db.utils.category import get_category_by_title, get_category_by_title_with_products
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.backend.utils.photo import upload_photo
from aiogram.types import PhotoSize
from aiogram import Bot


async def add_product(message_type: str, title: str, description: str, price: int, category_title: str,
                      session: AsyncSession, bot: Bot, photo: PhotoSize = None):
    category = await get_category_by_title(category_title, session)
    if category:
        uploaded_photo = None
        if photo:
            uploaded_photo = await upload_photo(photo, bot)
        new_product = Product(message_type=message_type, title=title, description=description, price=price,
                              photo=uploaded_photo, category=category)
        session.add(new_product)
        await session.commit()
        return new_product
    raise Exception('нет такой категории')


async def get_product_by_id(product_id: int, session: AsyncSession):
    return (await session.execute(select(Product).filter(Product.id == product_id))).scalar_one_or_none()


async def get_all_products(session: AsyncSession):
    return (await session.execute(select(Product))).scalars().all()


async def get_product_by_category(category_title: str, session: AsyncSession):
    category = await get_category_by_title_with_products(category_title, session)
    return category.products
