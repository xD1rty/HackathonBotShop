from core.backend.db.models.product import Product
from core.backend.db.utils.category import get_category_by_title, get_category_by_title_with_products
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def add_product(message_type: str, title: str, description: str, price: int, category_title: str,
                      session: AsyncSession, photo: str = None):
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


async def delete_product_by_id(product_id: int, session: AsyncSession):
    product = await get_product_by_id(product_id, session)
    await session.delete(product)
    return True


async def edit_product_by_id(product_id: int, session: AsyncSession, message_type: str = None, title: str = None,
                             description: str = None, price: int = None, category_title: str = None, photo: str = None):
    product = await get_product_by_id(product_id, session)
    if message_type:
        product.message_type = message_type
    if title:
        product.title = title
    if description:
        product.description = description
    if price:
        product.price = price
    if category_title:
        category = await get_category_by_title(category_title, session)
        if category:
            product.category = category
        raise Exception('нет такой категории')
    if photo:
        product.photo = photo
    await session.commit()
    return product


async def get_all_products(session: AsyncSession):
    return (await session.execute(select(Product))).scalars().all()


async def get_product_by_category(category_title: str, session: AsyncSession):
    category = await get_category_by_title_with_products(category_title, session)
    return category.products
