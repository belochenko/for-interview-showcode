from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from utils.db_api.data_manage import push_post_approval
from utils.misc.static_msg import msg
from states.posting import Post
from keyboards.default import buttons as btn


@dp.message_handler(content_types=types.ContentTypes.ANY, state=Post.approve)
async def approve_send(message: types.Message, state: FSMContext):
    """
    Sends post to database
    :param message:
    :param state:
    :return:
    """
    str_of_cids = str((await state.get_data()).get('set_of_cids'))[1:-1]  # cleaning brackets before pushing
    if message.text is not None and message.text == "Закончить":
        await message.answer(msg.stop, reply_markup=btn.void)
        await state.finish()
    else:
        await push_post_approval(message.from_user.id, message.message_id, str_of_cids)
        await message.answer(msg.post_done, reply_markup=btn.stop)
