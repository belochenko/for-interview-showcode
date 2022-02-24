from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from utils.misc.static_msg import msg
from keyboards.default import buttons as btn


@dp.message_handler(lambda message: message.text == 'Закончить', state="*")
async def stop(message: types.Message, state: FSMContext):
    """
    Stop current operations with the bot
    :param message:
    :param state:
    :return:
    """
    await message.answer(msg.stop, reply_markup=btn.void)
    await state.finish()
