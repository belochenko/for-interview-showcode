from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from utils.misc.static_msg import msg
from states.posting import Post
import keyboards.inline.posting as post_btn
from keyboards.default import buttons as btn
from utils.db_api.models import User, Groups
from data.config import ACCESS_ROLES
from wasabi import msg as log


@dp.message_handler(lambda message: (message.text == "Создать заявку на рассылку поста"
                    and getattr(User.get_or_none(message.chat.id == User.user_id), 'role', None) == ACCESS_ROLES[1])
                    or message.text == "Отправить пост без заявки"
                    and getattr(User.get_or_none(message.chat.id == User.user_id), 'role', None) == ACCESS_ROLES[2],
                    state='*')
async def chat_select(message: types.Message, state: FSMContext):
    """
    Show redactor list of groups ( inline buttons )
    :param message:
    :param state:
    :return:
    """
    if message.chat.id == message.from_user.id:
        await message.answer("Вы начали создавать пост", reply_markup=btn.stop)
        query = None
        try:
            query = Groups.select(Groups.group_id, Groups.group_major)
        except Exception as err:
            log.fail(f"{err}")
        list_of_groups = [row for row in query.tuples()]
        if len(list_of_groups) == 0:
            log.warn(f"Empty chats list given to user {message.from_user.id}")
        majors_num = {str(group_id): '✅    ' + major_name for (group_id, major_name) in list_of_groups}
        set_of_cids = {cids for cids, _ in list_of_groups}
        await message.answer('Выберите чаты!', reply_markup=post_btn.selected_chat(majors_num))
        await Post.chat_choose.set()
        await state.update_data(default=majors_num, set_of_cids=set_of_cids)


@dp.callback_query_handler(state=Post.chat_choose)
async def process_callback_chat_btn(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Processing callback from inline keyboard
    :param callback_query:
    :param state:
    :return:
    """
    response = callback_query.data
    user_data = await state.get_data()
    if response == 'next':
        if len(user_data['set_of_cids']) == 0:
            await callback_query.message.answer(msg.empty_list)
        elif getattr(User.get_or_none(callback_query.message.chat.id == User.user_id), 'role', None) == ACCESS_ROLES[1]:
            await Post.approve.set()
            await callback_query.message.answer(msg.choose_done, reply_markup=btn.stop)
        elif getattr(User.get_or_none(callback_query.message.chat.id == User.user_id), 'role', None) == ACCESS_ROLES[2]:
            await Post.posting.set()
            await callback_query.message.answer(msg.choose_done, reply_markup=btn.stop)
    else:
        if int(response) in user_data['set_of_cids']:
            user_data['set_of_cids'].discard(int(response))
        else:
            user_data['set_of_cids'].add(int(response))
        defdict = post_btn.check_btn_state(callback_query.data, (await state.get_data())['default'])
        await state.update_data(default=defdict, set_of_cids=user_data['set_of_cids'])
        await callback_query.message.edit_reply_markup(reply_markup=post_btn.selected_chat(defdict))


@dp.message_handler(content_types=types.ContentTypes.ANY, state=Post.posting)
async def post_send(message: types.Message, state: FSMContext):
    """
    Sends post to chats
    :param message:
    :param state:
    :return:
    """
    set_of_cids = (await state.get_data()).get('set_of_cids')
    if message.text is not None and message.text == "Закончить":
        await message.answer(msg.stop, reply_markup=btn.void)
        await state.finish()
    else:
        for cid in set_of_cids:
            try:
                await dp.bot.copy_message(cid, message.chat.id, message.message_id)
            except Exception as err:
                log.fail(f"Failed to send message to chat {cid}")
                log.fail(f"{err}")
        await message.answer(msg.admin_post_done, reply_markup=btn.stop)
