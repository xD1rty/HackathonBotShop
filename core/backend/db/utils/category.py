from core.backend.db.models.category import Category
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List


async def add_category(title: str, session: AsyncSession):
    if not await get_category_by_title(title, session):
        new_category = Category(title=title)
        session.add(new_category)
        await session.commit()
        return new_category
    raise Exception('такая категория уже есть')


async def get_category_by_title(title: str, session: AsyncSession):
    return (await session.execute(select(Category).filter(Category.title == title))).scalar_one_or_none()


async def get_category_by_title_with_products(title: str, session: AsyncSession):
    return (await session.execute(
        select(Category).filter(Category.title == title).options(selectinload(Category.products)))
            ).scalar_one_or_none()


async def get_all_category(session: AsyncSession):
    return (await session.execute(select(Category))).scalars().all()
