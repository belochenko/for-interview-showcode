from aiogram import types
from loader import dp


@dp.message_handler(content_types=types.ContentTypes.ANY, state='*')
async def bot_echo(message: types.Message):
    """
    Sends message if user entered
    incorrect data
    :param message:
    :return:
    """
    if message.chat.id == message.from_user.id:
        await message.answer("Данные введены неверно!")
