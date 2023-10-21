from aiogram.types import CallbackQuery
from aiogram import Bot
from core.backend.db.utils.order import add_order, get_order_by_id, change_order_status_by_id
from sqlalchemy.ext.asyncio import AsyncSession
from core.text import admin_order_request, user_order_done, user_order_request
from core.config import get_config
from core.backend.db.utils.user import get_user_by_id


async def create_order_request(
        call: CallbackQuery,
        bot: Bot,
        session: AsyncSession
):
        order = await add_order(call.from_user.id, int(call.data.replace("buy_", "").strip()), session)
        user = await get_user_by_id(order.user_id, session)
        await bot.send_message(get_config(".env").ADMIN_ID, admin_order_request.format(
            user_name = user.name,
            product_name = order.product.title
        ))
        await call.message.answer(user_order_request.format(
            product_name = order.product.title,
            price = order.product.price
        ))
