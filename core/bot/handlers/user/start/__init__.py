from aiogram import Bot, types, filters


async def start(
        bot: Bot,
        msg: types.Message,
        command: filters.Command):
    if command.args:
        pass
    else:
        ...
