from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from core.text import user_profile
from core.backend.db.utils.user import get_user_by_id


async def get_profile(
        message: Message,
        session: AsyncSession
):
    user = await get_user_by_id(message.from_user.id, session)
    if user != None and user.is_worker == True:
        await message.answer(user_profile.format(
            name=user.name,
            id=user.id,
            balance=user.balance,
            position=user.position
        ))
    else:
        await message.answer("Доступ запрещен!")