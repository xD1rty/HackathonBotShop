from core.backend.db.models.token import Token
from core.backend.db.utils.user import get_user_by_id
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from secrets import token_urlsafe


async def create_token(tg_id: int, money: int, session: AsyncSession):
    user = await get_user_by_id(tg_id, session)
    token = token_urlsafe()
    token_db = Token(token=token, money=money, user=user)
    session.add(token_db)
    await session.commit()
    return token_db


async def get_token(token: str, session: AsyncSession):
    return (await session.execute(select(Token).filter(Token.token == token))).scalar_one_or_none()


async def get_token_with_user(token: str, session: AsyncSession):
    return (await session.execute(select(Token).filter(Token.token == token).options(selectinload(Token.user)))).scalar_one_or_none()


async def use_token(tg_id: int, token: str, session: AsyncSession):
    token_db = await get_token_with_user(token, session)
    if token_db.is_open:
        user = await get_user_by_id(tg_id, session)
        money = token_db.money
        token_db.is_open = False
        token_db.user.balance -= money
        user.balance += money
        await session.commit()
        return True
    raise Exception('рефералка уже использована')
