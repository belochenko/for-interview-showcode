from loader import dp

from aiogram import types
from aiogram.dispatcher import FSMContext

from states.sign_up import SignUp
import keyboards.default.buttons as btn
from utils.misc.static_msg import msg, maj
from utils.db_api.data_manage import push_user
from utils.db_api.data_manage import db_user_check
import json
from wasabi import msg as log


@dp.message_handler(regexp='Зарегистрироваться', state=SignUp.is_reg)
async def reg(message: types.Message, state: FSMContext):
    """
    Starting register process or
    telling user that he's already registered
    :param message:
    :param state:
    :return:
    """
    if not await db_user_check('user_id', message.chat.id):
        await message.answer(msg.reg_phone_number, reply_markup=btn.phone_request)
        await SignUp.next()
    else:
        await message.answer(msg.already_reg, reply_markup=btn.void)
        await state.finish()


@dp.message_handler(state=SignUp.phone_number, content_types=types.ContentTypes.CONTACT)
async def get_phone_number(message: types.Message, state: FSMContext):
    """
    Adds phone number to state storage
    :param message:
    :param state:
    :return:
    """
    await state.update_data(phone_number=message.contact.phone_number)
    await message.answer(msg.reg_name_surname, reply_markup=btn.void)
    await SignUp.next()


@dp.message_handler(regexp=r'[А-Я][а-я]+\s[А-Я][а-я]+', state=SignUp.name_surname)
async def get_name_surname(message: types.Message, state: FSMContext):
    """
    Adds name and surname to state storage
    :param message:
    :param state:
    :return:
    """
    await state.update_data(name_surname=message.text)
    user_data = await state.get_data()
    if 'email' in user_data.keys():
        await submit(message, state)
    else:
        await message.answer(msg.reg_email, reply_markup=btn.void)
        await SignUp.next()


@dp.message_handler(regexp=r'[^\r\n\t\f\v\@]+@[^\r\n\t\f\v\@]+', state=SignUp.email)
async def email(message: types.Message, state: FSMContext):
    """
    Adds email to state storage
    :param message:
    :param state:
    :return:
    """
    if message.text.split('@')[1] != 'stud.onu.edu.ua':
        await message.answer(msg.reg_email_err)
        log.warn(f"User {message.from_user.id} tried to sign up with wrong email domain {message.text}")
    else:
        await state.update_data(email=message.text)
        user_data = await state.get_data()
        if 'year' in user_data.keys():
            await submit(message, state)
        else:
            await message.answer(msg.reg_study_year, reply_markup=btn.year_of_study)
            await SignUp.next()


@dp.message_handler(state=SignUp.year)
async def year(message: types.Message, state: FSMContext):
    """
    Adds learning year to state storage
    :param message:
    :param state:
    :return:
    """
    if message.text not in ['Курс 1', 'Курс 2', 'Курс 3', 'Курс 4', 'Курс 5', 'Курс 6']:
        await message.answer(msg.reg_year_err)
    else:
        await state.update_data(year=message.text)
        await message.answer(msg.reg_study_major, reply_markup=btn.mj_button)
        await SignUp.next()


@dp.message_handler(state=SignUp.major)
async def major(message: types.Message, state: FSMContext):
    """
    Adds major to state storage
    :param message:
    :param state:
    :return:
    """
    with open('data/major.json', encoding='utf-8') as f:
        data = json.load(f)
        lst_of_majs = [str(key[1:]) for key in data.keys()]
    if message.text not in lst_of_majs:
        await message.answer(msg.reg_major_err)
    else:
        form_maj = 'm' + message.text
        await state.update_data(major=getattr(maj, form_maj))
        await submit(message, state)


async def submit(message: types.Message, state: FSMContext):
    """
    Show user submit request
    :param message:
    :param state:
    :return:
    """
    async with state.proxy() as proxy:
        await message.answer(f"Ваша заявка:"
                             f"\n-Имя Фамилия: {proxy['name_surname']}"
                             f"\n-Почта: {proxy['email']}"
                             f"\n-Телефон: {proxy['phone_number']}"
                             f"\n-Специальность: [{proxy['year']}] {proxy['major']}", reply_markup=btn.choices)
    await SignUp.final.set()


@dp.message_handler(regexp='Изменить Имя и Фамилию', state=SignUp.final)
async def name_change(message: types.Message):
    """
    Changes name and returns to current request
    :param message:
    :return:
    """
    await message.answer(msg.reg_name_surname, reply_markup=btn.void)
    await SignUp.name_surname.set()


@dp.message_handler(regexp='Изменить почту', state=SignUp.final)
async def email_change(message: types.Message):
    """
    Changes email and returns to current request
    :param message:
    :return:
    """
    await message.answer(msg.reg_email, reply_markup=btn.void)
    await SignUp.email.set()


@dp.message_handler(regexp='Изменить курс и специальность', state=SignUp.final)
async def year_maj_change(message: types.Message):
    """
    Changes learning year and major
    :param message:
    :return:
    """
    await message.answer(msg.reg_study_year, reply_markup=btn.year_of_study)
    await SignUp.year.set()


@dp.message_handler(regexp='Зарегистрироваться заново', state=SignUp.final)
async def again(message: types.Message, state: FSMContext):
    """
    Reset state data and
    :param message:
    :param state:
    :return:
    """
    await message.answer(msg.reg_phone_number, reply_markup=btn.phone_request)
    await state.reset_data()
    await SignUp.phone_number.set()


@dp.message_handler(regexp='Верно, отправить данные!', state=SignUp.final)
async def reg_send_approval(message: types.Message, state: FSMContext):
    """
    Push data to database
    and finishes state
    :param message:
    :param state:
    :return:
    """
    user_data = await state.get_data()
    await push_user(username=message.chat.username,
                    first_name=user_data['name_surname'].split(' ')[0],
                    last_name=user_data['name_surname'].split(' ')[1],
                    phone_number=user_data['phone_number'],
                    email=user_data['email'],
                    learning_year=user_data['year'].split(' ')[1],
                    major=user_data['major'],
                    user_id=message.chat.id,
                    role=None,
                    is_approve=False
                    )
    await message.answer(msg.reg_done, reply_markup=btn.void)
    log.good(f"User {message.from_user.id} successfully finished sign up")
    await state.finish()
