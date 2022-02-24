from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from utils.misc.create_approve_lists import create_reg_list, create_post_list
import json

void = ReplyKeyboardRemove()

sign_up_button = ReplyKeyboardMarkup(resize_keyboard=True) \
    .add(KeyboardButton('Зарегистрироваться'))

phone_request = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Отправить свой контакт ☎️', request_contact=True)
)

year_of_study = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, keyboard=[
    [
        KeyboardButton('Курс 1'), KeyboardButton('Курс 2'), KeyboardButton('Курс 3')
    ],
    [
        KeyboardButton('Курс 4'), KeyboardButton('Курс 5'), KeyboardButton('Курс 6')
    ]
])

editor_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[
    [KeyboardButton('Создать заявку на рассылку поста')]
])

with open('data/major.json', encoding='utf-8') as f:
    data = json.load(f)
    lst_of_specs = [x[1:] for x in data.keys()]

list_of_majors_buttons = [[KeyboardButton(f'{x}') for x in data] for data in
                          [lst_of_specs[x:x + 3] for x in range(0, len(lst_of_specs), 3)]]
mj_button = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=list_of_majors_buttons)

choices = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[
    [
        KeyboardButton('Изменить Имя и Фамилию'),
        KeyboardButton('Изменить почту')
    ],
    [
        KeyboardButton('Изменить курс и специальность'),
        KeyboardButton('Зарегистрироваться заново')
    ],
    [KeyboardButton('Верно, отправить данные!')]
])

stop = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row('Закончить')

panel_start = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[
    [
        KeyboardButton('Войти в админ панель')
    ]
    ,
    [
        KeyboardButton('Отправить пост без заявки'),
    ]
])

admin_panel = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton('Рассмотреть заявки на регистрацию'),
        KeyboardButton('Рассмотреть заявки на рассылку')
    ],
    [KeyboardButton('Закончить')]
]
                                  )

post_choices = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton('Принять'),
        KeyboardButton('Отклонить')
    ],
    [KeyboardButton('Закончить')]
]
                                   )

reg_choices = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton('Принять в старосты'),
        KeyboardButton('Принять в редакторы'),
    ],
    [KeyboardButton('Отклонить')],
    [KeyboardButton('Закончить')]
]
                                  )


def reg_list_button_create():
    """
    Creates buttons from
    list of register requests
    :return reg_list_button:
    """
    reg_list, _ = create_reg_list()
    reg_list_button = ReplyKeyboardMarkup(resize_keyboard=True)
    for row in reg_list:
        reg_list_button.add(KeyboardButton(row))
    reg_list_button.row('Закончить')
    return reg_list_button


def post_list_button_create():
    """
    Creates buttons from
    list of post requests
    :return post_list_button:
    """
    names = create_post_list()
    formatted_2d_list = [names[x:x + 3] for x in range(0, len(names), 3)]  # 2d list with 3 elements per inner list
    post_list_button = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(f'{cnt1 + formatted_2d_list.index(rows) + cnt2 * 2}• {row[0]} {row[1]}') for cnt1, row in
         enumerate(rows, 1)] for cnt2, rows in enumerate(formatted_2d_list, 0)]
                                           )
    post_list_button.row('Закончить')
    return post_list_button
