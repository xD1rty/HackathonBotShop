from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot
from core.backend.db.utils.order import add_order, get_order_by_id, change_order_status_by_id
from sqlalchemy.ext.asyncio import AsyncSession
from core.text import admin_order_request, user_order_done, user_order_request
from core.config import get_config
from core.backend.db.utils.user import get_user_by_id, remove_money
from core.backend.db.utils.product import get_product_by_id


async def create_order_request(
        call: CallbackQuery,
        bot: Bot,
        session: AsyncSession
):
    product_id = int(call.data.replace("buy_", "").strip())
    user = await get_user_by_id(call.from_user.id, session)
    product = await get_product_by_id(product_id, session)
    if user.balance < product.price:
        await call.message.answer("Недостаточно денег!!! Нажмите /start")
        return
    else:
        order = await add_order(call.from_user.id, product_id, session)
    keyboard_verity = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Готов", callback_data=f"done_{order.id}"
        )]
    ])
    await bot.send_message(get_config(".env").ADMIN_ID, admin_order_request.format(
        user_name = user.name,
        id = user.id,
        product_name = product.title
    ), reply_markup=keyboard_verity)
    await call.message.answer(user_order_request.format(
        product_name = product.title,
        price = product.price
    ))


async def verify_order_request(
        call: CallbackQuery,
        bot: Bot,
        session: AsyncSession
):
    order = await get_order_by_id(int(call.data.replace("done_", "").strip()), session)
    product = await get_product_by_id(order.product_id, session)
    await remove_money(order.user_id, product.price, session)
    await change_order_status_by_id(order.id, True, session)
    await bot.send_message(order.user_id, user_order_done.format(
        product_name=product.title
    ))
    await call.message.answer(f"Пользователь <code>{order.user_id}</code> должен к вам обратиться по поводу <b>{product.title}</b>")















