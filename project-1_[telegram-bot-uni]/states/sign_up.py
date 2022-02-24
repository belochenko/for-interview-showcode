from aiogram.dispatcher.filters.state import State, StatesGroup


class SignUp(StatesGroup):
    is_reg = State()
    phone_number = State()
    name_surname = State()
    email = State()
    year = State()
    major = State()
    final = State()
