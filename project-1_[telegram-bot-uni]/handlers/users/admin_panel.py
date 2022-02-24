from aiogram import types
from aiogram.dispatcher import FSMContext


from loader import dp

from states.admin import Admin
from keyboards.default import buttons as btn
from utils.db_api.models import User, PostApproval, Groups
from utils.misc.static_msg import msg
from utils.misc.create_approve_lists import create_reg_list, create_post_list


@dp.message_handler(lambda message: message.text == "Войти в админ панель", state=Admin.start)
async def admin_panel(message: types.Message):
    """
    Creates button of admin panel and changes Admin state
    :param message:
    :return:
    """
    await message.answer(msg.admin_start, reply_markup=btn.admin_panel)
    await Admin.look.set()


@dp.message_handler(lambda message:
                    message.text in ['Рассмотреть заявки на регистрацию', 'Рассмотреть заявки на рассылку'],
                    state=Admin.look)
async def panel_look(message: types.Message):
    """
    Give administrator
    request accepting access
    :param message:
    :return:
    """
    if message.text == 'Рассмотреть заявки на регистрацию':

        _, regs_id = create_reg_list()
        if len(regs_id) > 0:
            await message.answer(msg.panel_notempty, reply_markup=btn.reg_list_button_create())
            await Admin.reg_approve.set()
        else:
            await message.answer(msg.reg_empty, reply_markup=btn.admin_panel)
    elif message.text == 'Рассмотреть заявки на рассылку':

        names = create_post_list()
        if len(names) > 0:
            await message.answer(msg.panel_notempty, reply_markup=btn.post_list_button_create())
            await Admin.post_approve.set()
        else:
            await message.answer(msg.postapp_empty, reply_markup=btn.admin_panel)


@dp.message_handler(lambda message: message.text is not None and message.text != "Закончить", state=Admin.reg_approve)
async def reg_approve(message: types.Message, state: FSMContext):
    """
    Show administrator registration request
    :param message:
    :param state:
    :return:
    """
    list_of_regs, regs_id = create_reg_list()
    if message.text in list_of_regs:
        user_approve = User.get_or_none(User.user_id == regs_id[list_of_regs.index(message.text)])
        await message.answer(f"\n-Имя Фамилия: {user_approve.first_name} {user_approve.last_name}"
                             f"\n-Почта: {user_approve.email}"
                             f"\n-Телефон: {user_approve.phoneNumber}"
                             f"\n-Специальность: [Курс {user_approve.learningYear}] {user_approve.Major}",
                             reply_markup=btn.reg_choices)
        await state.update_data(id=user_approve.user_id)
        await Admin.reg_final.set()
    else:
        await message.answer(msg.request_incorrect)


@dp.message_handler(lambda message: message.text in ['Принять в старосты', "Принять в редакторы", 'Отклонить'],
                    state=Admin.reg_final)
async def final_reg(message: types.Message, state: FSMContext):
    """
    Accept or Deny
    registration request
    :param message:
    :param state:
    :return:
    """
    user_id = (await state.get_data())['id']
    update = User.get_by_id(user_id)
    if message.text == 'Принять в старосты':
        update.is_approve = True
        update.role = 'group_lead'
        update.save()
        await dp.bot.send_message(user_id, msg.reg_glead_success)
    elif message.text == 'Принять в редакторы':
        update.is_approve = True
        update.role = 'editor'
        update.save()
        await dp.bot.send_message(user_id, msg.reg_editor_success)
    else:
        update.delete_instance()
        await dp.bot.send_message(user_id, msg.reg_refuse)
    _, regs_id = create_reg_list()
    if len(regs_id) > 0:
        await message.answer(msg.panel_notempty, reply_markup=btn.reg_list_button_create())
        await Admin.reg_approve.set()
    else:
        await message.answer(msg.reg_empty, reply_markup=btn.admin_panel)
        await Admin.look.set()


@dp.message_handler(lambda message: message.text is not None and message.text != "Закончить", state=Admin.post_approve)
async def post_approve(message: types.Message, state: FSMContext):
    """
    Show administrator post request
    :param message:
    :param state:
    :return:
    """
    post_approvals = create_post_list()  # list of tuples of post_approvals
    choices = [f'{cnt}• {post_approval[0]} {post_approval[1]}' for cnt, post_approval in enumerate(post_approvals, 1)]
    if message.text in choices:
        chosen_post_approval = int(message.text.split('•')[0]) - 1  # chosen index for tuple in list of tuples
        post_approval = post_approvals[chosen_post_approval]  # chosen tuple
        user_id, message_id, chats = post_approval[2], post_approval[3], post_approval[4].split(', ')
        query = Groups.select(Groups.group_major).where(Groups.group_id << [int(chat) for chat in chats])
        chatnames = [row.group_major for row in query]
        chat_str = ''
        for chat in chatnames:
            chat_str += f', \n- {chat}'
        mess_id = await dp.bot.forward_message(message.chat.id, user_id, message_id)
        await message.answer(f"В чаты {chat_str[2:]}", reply_markup=btn.post_choices)
        await state.update_data(msg=mess_id, chats=chats, msg_id=message_id)
        await Admin.post_final.set()
    else:
        await message.answer(msg.request_incorrect, reply_markup=btn.post_list_button_create())


@dp.message_handler(lambda message: message.text in ["Принять", "Отклонить"] and message.text != "Закончить",
                    state=Admin.post_final)
async def final_post(message: types.Message, state: FSMContext):
    """
    Accept or Deny post request
    :param message:
    :param state:
    :return:
    """
    mess = (await state.get_data()).get('msg')
    chats = (await state.get_data()).get('chats')
    msg_id = (await state.get_data()).get('msg_id')
    if message.text == 'Принять':
        for chat in chats:
            await dp.bot.copy_message(chat, message.chat.id, mess.message_id)
        await dp.bot.copy_message(mess.forward_from.id, message.chat.id, mess.message_id)
        await dp.bot.send_message(mess.forward_from.id, msg.postapp_success)
    else:
        await dp.bot.copy_message(mess.forward_from.id, message.chat.id, mess.message_id)
        await dp.bot.send_message(mess.forward_from.id, msg.postapp_refuse)
    PostApproval.get(PostApproval.post_message_id == msg_id).delete_instance()
    names = create_post_list()
    if len(names) > 0:
        await message.answer(msg.panel_notempty, reply_markup=btn.post_list_button_create())
        await Admin.post_approve.set()
    else:
        await message.answer(msg.postapp_empty, reply_markup=btn.admin_panel)
        await Admin.look.set()
