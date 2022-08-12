from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class Condition(StatesGroup):
    home = State()
    fork = State()
    document = State()
    question = State()
    prise = State()
    agree = State()
    registration_n = State()
    registration_s = State()
    registration_age = State()
    confirm_user = State()
