from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp

from data.config import ACCESS_ROLES
from utils.misc.static_msg import msg
from states.sign_up import SignUp
from states.admin import Admin
import keyboards.default.buttons as btn
from utils.db_api.models import User
from wasabi import msg as log


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message):
    """
    Starts dialogue with user
    according to its role in database
    :param message:
    :return:
    """
    if message.chat.id == message.from_user.id:
        query = User.get_or_none(User.user_id == message.chat.id)
        if query is not None:
            user_role = User.get_or_none(User.user_id == message.chat.id).role
            if user_role == ACCESS_ROLES[0]:
                await message.answer(msg.approved_glead, reply_markup=btn.void)
            elif user_role == ACCESS_ROLES[1]:
                await message.answer(msg.approved_red, reply_markup=btn.editor_button)
            elif user_role == ACCESS_ROLES[2]:
                await message.answer(msg.approved_admin, reply_markup=btn.panel_start)
                await Admin.start.set()
            else:
                await message.answer(msg.already_reg, reply_markup=btn.void)
        else:
            log.info(f'User {message.from_user.id} started to sign up')
            await message.answer(msg.start, reply_markup=btn.sign_up_button)
            await SignUp.is_reg.set()


