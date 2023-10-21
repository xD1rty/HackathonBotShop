from aiogram.types import Message
from aiogram import Bot
from core.bot.states.admin.category import CreateCategory
from core.bot.states.admin.product import CreateProduct
from core.backend.db.utils.category import add_category, get_all_category, get_category_by_title
from core.backend.db.utils.product import add_product
from sqlalchemy.ext.asyncio import AsyncSession
from core.config import get_config
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from core.backend.utils.photo import upload_photo
from aiogram.types import InputFile
from core.text import product_text
from core.bot.keyboards.reply import admin_menu
from aiogram.enums.content_type import ContentType


async def create_category(
        message: Message,
        state: FSMContext,
):
    if message.from_user.id == get_config(".env").ADMIN_ID:
        await message.answer("Введите имя новой категории:")
        await state.set_state(CreateCategory.name)
    else:
        await message.answer("Доступ запрещен")

async def get_name_category(
        message: Message,
        state: FSMContext,
        session: AsyncSession
):
    res = await add_category(message.text, session)
    await message.answer(f"Категория {res.title} добавлена!")
    await state.clear()


async def create_product(
        message: Message,
        state: FSMContext
):
    if message.from_user.id == get_config(".env").ADMIN_ID:
        await message.answer("Введите название товара:")
        await state.set_state(CreateProduct.title)

    else:
        await message.answer("Доступ запрещен")


async def create_product_name(
        message: Message,
        state: FSMContext
):
    await state.update_data(title=message.text)
    await message.answer("Введите описание товара:")
    await state.set_state(CreateProduct.description)


async def create_product_desc(
        message: Message,
        state: FSMContext
):
    await state.update_data(description=message.text)
    await message.answer("Введите цену:")
    await state.set_state(CreateProduct.price)


async def create_product_price(
        message: Message,
        state: FSMContext,
        session: AsyncSession
):
    try:
        print(await get_all_category(session))
        k = ReplyKeyboardMarkup(
           keyboard=[[KeyboardButton(text=i.title) for i in await get_all_category(session)]]
        )
        await state.update_data(price=int(message.text))
        await message.answer("Выберите категорию:", reply_markup=k)
        await state.set_state(CreateProduct.category)

    except :
        ...

async def create_product_category(
        message: Message,
        state: FSMContext,
        session: AsyncSession
):
    if message.text in [i.title for i in await get_all_category(session)]:
        await state.update_data(category=message.text)
        await message.answer("Отправьте фотографию (ОДНУ), если не хотите, нажмите нет", reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Нет")]]))
        await state.set_state(CreateProduct.photos)

    else:
        await message.answer("Отправьте из списка!!!")


async def create_product_photos(
        message: Message,
        state: FSMContext,
        session: AsyncSession,
        bot: Bot
):
    if message.content_type == ContentType.TEXT:
        await state.update_data(photos=None)
    elif message.content_type == ContentType.PHOTO:
        urls = await upload_photo(message.photo[-1], bot)
        await state.update_data(photos=urls)

    data = await state.get_data()
    await state.clear()
    if data["photos"] == None:
        product = await add_product(
        message_type="text" ,
        title=data["title"],
        description=data["description"],
        category_title=data["category"],
        price=data["price"],
        session=session,
        bot=bot
        )

    if data["photos"] != None:
        product = await add_product(
            message_type="photo",
            title=data["title"],
            description=data["description"],
            category_title=data["category"],
            price=data["price"],
            photo=data["photos"],
            session=session,
            bot=bot
        )
    if product.photo != None:
        await message.answer_photo(photo=InputFile(product.photo), caption=product_text.
                                   format(
            name = product.title,
            description = product.description,
            price = product.price,
            category = product.category
        ), reply_markup=admin_menu)
    else:
        await message.answer(product_text.
                           format(
            name=product.title,
            description=product.description,
            price=product.price,
            category=product.category
        ), reply_markup=admin_menu)
