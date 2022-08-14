from aiogram import Bot, types, Dispatcher, executor
from aiogram.utils.executor import start_webhook
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from states import Condition, FSMContext
import keyboard
import logging
from info_parse import search_procedure
import os

storage = MemoryStorage()
TOKEN = os.getenv('BOT_TOKEN')
TOKEN = str(TOKEN)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

# настройки вебхука
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# настройки сервера
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)


async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dispatcher):
    await bot.delete_webhook()


@dp.message_handler(commands=['start', 'help'], state='*')
async def start_menu(message: types.Message):
    await bot.send_message(message.chat.id, 'Чем могу помочь?', reply_markup=keyboard.menu)
    await Condition.fork.set()


@dp.message_handler(state=Condition.home)
async def home_page(message: types.Message):
    await bot.send_message(message.chat.id, 'Чем могу помочь?', reply_markup=keyboard.menu)
    await Condition.fork.set()


@dp.message_handler(state=Condition.fork)
async def way(message: types.Message, state: FSMContext):
    if message.text.lower() == 'прайс':
        await bot.send_message(message.chat.id, f'Ранняя версия каталога услуг:'
                                                f'\n1)Аппаратная чистка\n'
                                                f'2)Пиллинг лица\n3)Косметический массаж\n'
                                                f'4)Биоревитализация\n5)Криотерапия\n'
                                                f'6)СМАС-лифтинг для лица\n\n'
                                                f'Введите номер интересующей вас процедуры', reply_markup=keyboard.q_or_home)
        await Condition.prise.set()
    elif message.text.lower() == 'задать вопрос':
        await Condition.question.set()
        await bot.send_message(message.chat.id, 'Введите ваш вопрос', reply_markup=keyboard.ReplyKeyboardRemove())


@dp.message_handler(state=Condition.question)
async def users_question(message: types.Message, state: FSMContext):
    chat_id = '1505714650'  # добавить нужный id
    await bot.send_message(chat_id, "@" + message.from_user.username + ": " + message.text)
    await Condition.fork.set()
    await bot.send_message(message.chat.id, 'Виталия свяжется с вами и ответит на вопрос', reply_markup=keyboard.menu)


@dp.message_handler(state=Condition.prise)
async def number_of_procedure(message: types.Message, state: FSMContext):

    if message.text.lower() != 'в меню' and message.text.lower() != 'задать вопрос':
        count_of_procedure = []
        for i in range(10):
            count_of_procedure.append(str(i))

        if message.text in count_of_procedure:
            number = message.text
            await bot.send_message(message.chat.id, search_procedure('procedure_description_all.txt', number))
            await state.update_data(prise=number)
            await Condition.agree.set()
            await bot.send_message(message.chat.id, 'Вы выбрали процедуру, давайте вас запишем', reply_markup=keyboard.agree)

    elif message.text.lower() == 'задать вопрос':
        await Condition.question.set()
        await bot.send_message(message.chat.id, 'Введите вопрос', reply_markup=keyboard.ReplyKeyboardRemove())

    else:
        await Condition.fork.set()
        await bot.send_message(message.chat.id, 'Выберите категорию снова', reply_markup=keyboard.menu)


@dp.message_handler(state=Condition.agree)
async def user_agree(message: types.Message, state: FSMContext):
    if message.text.lower() == 'записаться' or message.text.lower() == 'вперед':
        await Condition.registration_n.set()
        await bot.send_message(message.chat.id, 'Введите имя', reply_markup=keyboard.ReplyKeyboardRemove())
    elif message.text.lower() == 'в меню':
        await Condition.home.set()
    elif message.text.lower() == 'назад':
        await Condition.prise.set()
        await bot.send_message(message.chat.id, 'Введите номер процедуры')


@dp.message_handler(state=Condition.registration_n)
async def registration_name(message: types.Message, state: FSMContext):
    name = message.text.strip()
    await state.update_data(registration_n=name)
    await Condition.registration_s.set()
    await bot.send_message(message.chat.id, 'Введите фамилию')


@dp.message_handler(state=Condition.registration_s)
async def registration_surname(message: types.Message, state: FSMContext):
    surname = message.text.strip()
    await state.update_data(registration_s=surname)
    await Condition.registration_age.set()
    await bot.send_message(message.chat.id, 'Введите возраст')


@dp.message_handler(state=Condition.registration_age)
async def registration_age(message: types.Message, state: FSMContext):
    global number_user, name_user, surname_user, age_user
    age = message.text.strip()
    await state.update_data(registration_age=age)
    data = await state.get_data()
    number_user = data.get('prise')
    number_user = search_procedure('procedure_d.txt', number_user)
    name_user = data.get('registration_n')
    surname_user = data.get('registration_s')
    age_user = data.get('registration_age')
    await Condition.confirm_user.set()
    await bot.send_message(message.chat.id, f'Данные верны: {name_user} {surname_user} в возрасте {age_user}'
                                            f' записан(а) на процедуру \'{number_user}\'', reply_markup=keyboard.confirm)


@dp.message_handler(state=Condition.confirm_user)
async def confirming(message: types.Message, state: FSMContext):
    if message.text.lower() == 'да':
        chat_id = '1505714650'  # добавить нужный id
        info = f'{name_user} {surname_user} в возрасте {age_user} записан(а) на процедуру \'{number_user}\''
        await bot.send_message(chat_id, "@" + message.from_user.username + ": " + info)
        await Condition.fork.set()
        await bot.send_message(message.chat.id, 'С вами свяжутся', reply_markup=keyboard.menu)

    elif message.text.lower() == 'нет':
        await Condition.agree.set()
        await bot.send_message(message.chat.id, 'Давайте попробуем еще раз', reply_markup=keyboard.reset)


if __name__ == '__main__':
    name_user = surname_user = number_user = age_user = ''
    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
