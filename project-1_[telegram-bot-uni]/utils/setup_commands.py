from aiogram import Dispatcher, types
import json


async def on_startup_commands(dp: Dispatcher):
    """
    Set commands to a bot
    :param dp:
    :return:
    """
    with open('data/commands.json', encoding='utf-8') as f:
        data = json.load(f)
    commands = [types.BotCommand(command=k, description=w) for k, w in data.items()]

    await dp.bot.set_my_commands(commands)


