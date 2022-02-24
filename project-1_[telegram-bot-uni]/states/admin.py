from aiogram.dispatcher.filters.state import State, StatesGroup


class Admin(StatesGroup):
    start = State()
    look = State()
    reg_approve = State()
    post_approve = State()
    reg_final = State()
    post_final = State()
