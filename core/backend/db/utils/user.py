from core.backend.db.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def register(tg_id: int, telegram_tag: str, name: str, position: str, session: AsyncSession):
    if not await get_user(tg_id, session):
        new_user = User(id=tg_id, telegram_tag=telegram_tag, name=name, position=position)
        session.add(new_user)
        await session.commit()
        return new_user
    raise Exception('юзер уже зареган')


async def get_user(tg_id: int, session: AsyncSession):
    return (await session.execute(select(User).filter(User.id == tg_id))).scalar_one_or_none()


async def get_all_users(session: AsyncSession):
    return (await session.execute(select(User))).scalars().all()


async def edit_status(tg_id: int, status: bool, session: AsyncSession):
    user = await get_user(tg_id, session)
    user.is_worker = status
    await session.commit()
    return True


async def add_money(tg_id: int, money: int, session: AsyncSession):
    user = await get_user(tg_id, session)
    user.balance += money
    await session.commit()
    return True
