from core.backend.db.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def register(tg_id: int, telegram_tag: str, name: str, position: str, session: AsyncSession):
    if not await get_user(tg_id, session):
        new_user = User(id=tg_id, telegram_tag=telegram_tag, name=name, position=position)
        session.add(new_user)
        await session.commit()
        return new_user


async def get_user(tg_id: int, session: AsyncSession):
    return (await session.execute(select(User).filter(User.id == tg_id))).scalar_one_or_none()
