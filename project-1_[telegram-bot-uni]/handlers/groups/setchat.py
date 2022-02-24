from loader import dp

from aiogram import types

from utils.db_api.models import User, Groups
from utils.db_api.data_manage import push_group
from data.config import ACCESS_ROLES


@dp.message_handler(commands=['setchat'])
async def set_chat(message: types.Message):
    """
    Adds chat to a database, to send info in it.

    :param message:
    :return:
    :rtype:
    """
    if message.chat.id != message.from_user.id :
        if getattr(User.get_or_none(User.user_id == message.from_user.id), 'role', None) in ACCESS_ROLES:
            query = Groups.get_or_none(Groups.group_id == message.chat.id)
            if query is None:
                user_maj = User.get_by_id(message.from_user.id)
                await push_group(group_id=message.chat.id,
                                 group_major=f'[Курс {user_maj.learningYear}] {user_maj.Major}',
                                 group_title=message.chat.title,
                                 group_user_id=message.from_user.id)
                await message.answer("Чат авторизован")
            else:
                await message.answer("Чат уже был авторизован!")

