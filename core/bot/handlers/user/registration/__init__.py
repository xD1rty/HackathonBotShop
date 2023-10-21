from aiogram import Bot, types, filters
from sqlalchemy.ext.asyncio import AsyncSession
from core.bot.states.user.registration import Registration
from core.text import reg_name, reg_position, reg_finish, admin_user_request
from core.config import get_config
from aiogram.fsm.context import FSMContext
from core.backend.db.utils.user import register, get_user_by_id
from core.bot.keyboards.inline import create_keyboard_accept_user


async def start_registration(
        message: types.Message,
        bot: Bot,
        state: FSMContext
):
    await message.answer(reg_name)
    await state.set_state(Registration.name)

async def get_name(
        message: types.Message,
        bot: Bot,
        state: FSMContext,
):
    await message.answer(reg_position)
    await state.update_data(name=message.text)
    await state.set_state(Registration.position)

async def get_position(
        message: types.Message,
        bot: Bot,
        state: FSMContext,
        session: AsyncSession
):
    await message.answer(reg_finish)
    await state.update_data(position=message.text)
    data = await state.get_data()
    user = await register(
        tg_id=message.from_user.id,
        telegram_tag=message.from_user.username,
        name=data["name"],
        position=data["position"],
        session=session
    )
    await bot.send_message(get_config(".env").ADMIN_ID,
                           admin_user_request.format(
                               name=user.name,
                               position=user.position,
                               id=user.id,
                               telegram_tag=user.telegram_tag),
                           reply_markup=create_keyboard_accept_user(message.from_user.id))
    await state.clear()