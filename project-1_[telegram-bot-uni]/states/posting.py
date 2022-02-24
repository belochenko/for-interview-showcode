from aiogram.dispatcher.filters.state import State, StatesGroup


class Post(StatesGroup):
    chat_choose = State()
    approve = State()
    posting = State()
