from aiogram.dispatcher.filters.state import State, StatesGroup


class ReklamaState(StatesGroup):
    rek = State()


class FindUser(StatesGroup):
    user_id = State()
