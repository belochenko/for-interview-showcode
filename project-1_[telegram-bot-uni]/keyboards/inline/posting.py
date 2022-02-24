from aiogram.types import InlineKeyboardButton, \
    InlineKeyboardMarkup


def selected_chat(all_chats: dict):
    """
    Creates inline buttons fo
    :param all_chats:
    :return chats:
    """
    chats_btn = [
        [InlineKeyboardButton(text=chat_name, callback_data=btn_num)]
        for btn_num, chat_name in all_chats.items()
    ]
    chats_btn.append([InlineKeyboardButton(text='Далее', callback_data='next')])
    chats = InlineKeyboardMarkup(inline_keyboard=chats_btn)
    return chats


def check_btn_state(btn_callback_data: str, default: dict):
    """
    Checks what state in button
    :param btn_callback_data:
    :param default:
    :return default:
    """
    current = default.get(btn_callback_data)
    if current[0] == '✅':
        default.update({btn_callback_data: '❌' + current[1:]})
    else:
        default.update({btn_callback_data: '✅' + current[1:]})
    return default
