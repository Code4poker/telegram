from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Задать вопрос')],
              [KeyboardButton(text='Прайс')]],
    resize_keyboard=True, row_width=1
)

q_or_home = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='В меню')],
              [KeyboardButton(text='Задать вопрос')]],
    resize_keyboard=True, row_width=1
)


agree = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Назад')],
              [KeyboardButton(text='Записаться')]],
    resize_keyboard=True, row_width=1
)

confirm = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Да')],
              [KeyboardButton(text='Нет')]],
    resize_keyboard=True, row_width=1
)

reset = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Вперед')],
              [KeyboardButton(text='В меню')]],
    resize_keyboard=True, row_width=1
)