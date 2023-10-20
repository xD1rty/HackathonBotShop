from aiogram import Bot, types, filters
from core.bot.states.user.registration import Registration
from core.text import reg_name, reg_position, reg_finish, admin_user_request
from core.config import get_config
from aiogram.fsm.context import FSMContext


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
        state: FSMContext
):
    await message.answer(reg_position)
    await state.update_data(name=message.text)
    await state.set_state(Registration.position)

async def get_position(
        message: types.Message,
        bot: Bot,
        state: FSMContext
):
    await message.answer(reg_finish)
    await state.update_data(position=message.text)
    data = await state.get_data()
    await bot.send_message(get_config(".env").ADMIN_ID, admin_user_request.format(name=data["name"], position=data["position"], id=message.from_user.id, telegram_tag=message.from_user.username))
    await state.clear()