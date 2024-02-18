from random import shuffle, choice

from aiogram import Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from db_main import session
from db_models import new_user, get_word, add_word, del_word
from keyboards import *
from fsm_forms import *

dp = Dispatcher()

# Этот хендлер будет срабатывать на команду "/start"
async def process_start_command(message: Message):
    new_user(session, message)  #запись нового юзера в базу данных
    button_1 = KeyboardButton(text='Начать')
    button_2 = KeyboardButton(text='/help')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button_1, button_2]], resize_keyboard=True, one_time_keyboard=True)
    await message.answer(
    'Привет 👋 Давай попрактикуемся в английском языке. ' 
    'Тренировки можешь проходить в удобном для себя темпе.',
    reply_markup=keyboard
)

# Этот хендлер будет срабатывать на команду "/help"
async def process_help_command(message: Message):
    
    builder = ReplyKeyboardBuilder().add(KeyboardButton(text='Начать'))

    await message.answer(
        'У тебя есть возможность использовать тренажёр, как конструктор, '
        'и собирать свою собственную базу для обучения. Для этого воспрользуйся инструментами:\n'
        '- добавить слово ➕,\n'
        '- удалить слово 🔙.\n'
        'Ну что, начнём ⬇️',
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
    )

# Этот хендлер будет срабатывать на кнопку "начать"
async def process_start_words(message: Message, state: FSMContext):
    word = get_word(session, message)   # Получаем случайное слово из базы
    await state.set_state(CheckTranslate.tr_word)
    await state.update_data(tr_word=word)
    var_buttons = [
        word.tr, word.var_1, word.var_2, word.var_3
    ]
    builder = keyboard_builder(var_buttons)
    await state.set_state(CheckTranslate.var)
    await message.answer(
        f'Выбери перевод слова:\n"{word.word}"',
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
    )

# Этот хендлер проверяет вариант ответа на правильность
async def process_check_translate(message: Message, state: FSMContext):
    await state.update_data(var=message.text)
    data = await state.get_data()
    word = data.get('tr_word')
    if message.text.lower() == word.tr.lower():
        builder = main_buttons()
        answer = ['Правильно!', 'Совершенно верно!', 'Точно!', 'Отлично!', 'Прекрасно!']
        await state.clear()
        await message.answer(
            f'{choice(answer)} Продолжаем?', 
            reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
        )
    else:
        var_buttons = [
        word.tr, word.var_1, word.var_2, word.var_3
    ]
        builder = keyboard_builder(var_buttons)
        answer = ['Неверный ответ', 'Неправильный ответ', 'Неправильно']
        await state.set_state(CheckTranslate.var)
        await message.answer(
            f'{choice(answer)}, попробуйте еще раз\n'
            f'Слово "{word.word}"',
            reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
        )

# Этот хендлер начинает процесс удаления слова
async def delete_word(message: Message, state: FSMContext):
    await state.clear()
    builder = ReplyKeyboardBuilder().add(KeyboardButton(text='/cancel'))
    await message.answer(
        'Введите слово на русском 🇷🇺 которое нужно удалить '
        'или нажмите /cancel если передумали',
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
    )
    await state.set_state(WordToDelete.word_to_del)


# Этот хендлер начинает процесс добавления нового слова
async def process_word_fillform(message: Message, state: FSMContext):
    await state.clear()
    builder = ReplyKeyboardBuilder().add(KeyboardButton(text='/cancel'))
    await message.answer(
        text='Введите слово на русском 🇷🇺\n'
        'Или нажмите /cancel для отмены',
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
    )
    await state.set_state(AddWordForm.word)

# Если пользователь передумал добавлять слово и нажал /cancel
async def process_cancel(message: Message, state: FSMContext):
    builder = ReplyKeyboardBuilder().add(KeyboardButton(text='Дальше ⏭'))
    await message.answer(
        text='Чтобы вернуться к изучению слов, '
             'нажмите "Дальше ⏭"',
             reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
    )
    await state.clear()

# Этот хендлер получает слово, которое нужно удалить, и удаляет его
async def process_word_delete(message: Message, state: FSMContext):
    word_to_del = message.text
    result = del_word(session, message, word_to_del)    # Удаляет слово из базы
    await state.clear()
    builder = ReplyKeyboardBuilder().add(KeyboardButton(text='Дальше ⏭'))
    await message.answer(
        text=result,
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
    )

async def process_word_sent(message: Message, state: FSMContext):
    builder = ReplyKeyboardBuilder().add(KeyboardButton(text='/cancel'))
    await state.update_data(word=message.text)
    await message.answer(
        text='Теперь введите правильный перевод слова на английском 🇬🇧',
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
    )
    await state.set_state(AddWordForm.tr)

async def process_tr_sent(message: Message, state: FSMContext):
    builder = ReplyKeyboardBuilder().add(KeyboardButton(text='/cancel'))
    await state.update_data(tr=message.text)
    await message.answer(
        text='Введите первый вариант неправильного перевода на английский',
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
    )
    await state.set_state(AddWordForm.var_1)

async def process_var_1_sent(message: Message, state: FSMContext):
    builder = ReplyKeyboardBuilder().add(KeyboardButton(text='/cancel'))
    await state.update_data(var_1=message.text)
    await message.answer(
        text='Введите второй вариант неправильного перевода на английский',
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
    )
    await state.set_state(AddWordForm.var_2)

async def process_var_2_sent(message: Message, state: FSMContext):
    builder = ReplyKeyboardBuilder().add(KeyboardButton(text='/cancel'))
    await state.update_data(var_2=message.text)
    await message.answer(
        text='Введите третий вариант неправильного перевода на английский',
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
    )
    await state.set_state(AddWordForm.var_3)

async def process_var_3_sent(message: Message, state: FSMContext):
    builder = ReplyKeyboardBuilder().add(KeyboardButton(text='Дальше ⏭'))
    await state.update_data(var_3=message.text)
    added_word = await state.get_data()
    add_word(session, message, added_word)  # Добавляет слово в базу
    await state.clear()
    await message.answer(
        text='Спасибо! Новое слово добавлено. '
        'Чтобы вернуться к изучению слов, '
        'нажмите "Дальше ⏭"',
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
    )

# Обрабатывает сообщения, которые не попали в фильтры
async def other_messages(message: Message):
    builder = ReplyKeyboardBuilder().add(KeyboardButton(text='Начать'))
    await message.answer(
        'Не знаю такой команды.\n'
        'Нажмите "Начать", чтобы запустить тренажер',
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
    )
    