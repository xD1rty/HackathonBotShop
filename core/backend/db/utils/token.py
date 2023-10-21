from core.backend.db.models.token import Token
from core.backend.db.utils.user import get_user
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from secrets import token_urlsafe


async def create_token(tg_id: int, money: int, session: AsyncSession):
    user = await get_user(tg_id, session)
    token = token_urlsafe(16)
    token_db = Token(token=token, money=money, user=user)
    session.add(token_db)
    await session.commit()
    return token


async def get_token(token: str, session: AsyncSession):
    return (await session.execute(select(Token).filter(Token.token == token))).scalar_one_or_none()


async def use_token(tg_id: int, token: str, session: AsyncSession):
    token_db = await get_token(token, session)
    user = await get_user(tg_id, session)
    money = token_db.money
    token_db.user.balance -= money
    user.balance += money
    await session.commit()
    return True
