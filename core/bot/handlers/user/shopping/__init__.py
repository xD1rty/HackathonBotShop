from aiogram import Bot
from aiogram.types import Message, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, \
    CallbackQuery
from aiogram.fsm.context import FSMContext
from core.backend.db.utils.product import get_product_by_category
from core.backend.db.utils.category import get_all_category
from sqlalchemy.ext.asyncio import AsyncSession
from core.text import product_text
from core.bot.states.user.shopping import GetProductsByCategory
from core.backend.db.utils.user import get_user_by_id


async def get_product_by_category_start(
        message: Message,
        bot: Bot,
        state: FSMContext,
        session: AsyncSession
):
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=i.title)] for i in await get_all_category(session)
    ])
    await message.answer("Выберите нужную вам категорию:", reply_markup=keyboard)
    await state.set_state(GetProductsByCategory.category)

async def get_all_products_by_category(
        message: Message,
        bot: Bot,
        state: FSMContext,
        session: AsyncSession
):
    if message.text in [i.title for i in await get_all_category(session)]:
        await state.clear()
        products = await get_product_by_category(message.text, session)
        for product in products:
            keyboard_inline = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Купить", callback_data=f"buy_{product.id}")
                ]
            ])
            if product.photo is not None:
                await message.answer_photo(photo=product.photo, caption=product_text.
                                           format(
                    name=product.title,
                    description=product.description,
                    price=product.price,
                    category=message.text
                ), reply_markup=keyboard_inline)
            else:
                await message.answer(product_text.
                format(
                    name=product.title,
                    description=product.description,
                    price=product.price,
                    category=message.text
                ), reply_markup=keyboard_inline)
    else:
        await message.answer("Введите корректное значение")
