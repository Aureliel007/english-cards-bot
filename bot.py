from random import shuffle, choice
from configparser import ConfigParser

from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, ContentType
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import F


# Вместо BOT TOKEN HERE нужно вставить токен вашего бота, полученный у @BotFather
config = ConfigParser()
config.read('config.ini')
BOT_TOKEN = config['TGBot']['token']

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

words = [
    {'word': 'Она', 'tr': 'She', 'var_1': 'We', 'var_2': 'Her', 'var_3': 'He'},
    {'word': 'Стол', 'tr': 'Table', 'var_1': 'Chair', 'var_2': 'Stool', 'var_3': 'Boat'},
    {'word': 'Юбка', 'tr': 'Skirt', 'var_1': 'Dress', 'var_2': 'Wear', 'var_3': 'Coat'},
    {'word': 'Зонт', 'tr': 'Umbrella', 'var_1': 'Raincoat', 'var_2': 'Jacket', 'var_3': 'Sword'},
    {'word': 'Кукла', 'tr': 'Doll', 'var_1': 'Toy', 'var_2': 'Barbie', 'var_3': 'Thing'},
    {'word': 'Творог', 'tr': 'Cottage cheese', 'var_1': 'Cheese', 'var_2': 'Sour cream', 'var_3': 'Milk'},
    {'word': 'Хурма', 'tr': 'Persimmon', 'var_1': 'Eggplant', 'var_2': 'Orange', 'var_3': 'Pineapple'},
    {'word': 'Помада', 'tr': 'Lipctick', 'var_1': 'Lipgloss', 'var_2': 'Pencil', 'var_3': 'Stick'},
    {'word': 'Змея', 'tr': 'Snake', 'var_1': 'Python', 'var_2': 'Boa', 'var_3': 'Anaconda'}
]
users = {'user_id': {'words': [], 'current_word': 'word_id'}}

def keyboard_builder(var_buttons: list):
    builder = ReplyKeyboardBuilder()
    shuffle(var_buttons)
    main_buttons = ['Добавить слово ➕', 'Удалить слово 🔙', 'Дальше ⏭']
    for button in var_buttons:
        builder.add(KeyboardButton(text=button))
    for button in main_buttons:
        builder.add(KeyboardButton(text=button))
    builder.adjust(2, 2, 2, 1)
    return builder

def main_buttons():
    main_buttons = ['Добавить слово ➕', 'Удалить слово 🔙', 'Дальше ⏭']
    builder = ReplyKeyboardBuilder()
    for button in main_buttons:
        builder.add(KeyboardButton(text=button))
    builder.adjust(2, 1)
    return builder

class AddWordForm(StatesGroup):
    word = State()
    tr = State()
    var_1 = State()
    var_2 = State()
    var_3 = State()

class CheckTranslate(StatesGroup):
    tr_word = State()
    var = State()

class WordToDelete(StatesGroup):
    word_to_del = State()

# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(CommandStart())
async def process_start_command(message: Message):
    if message.from_user.id not in users:
        users[message.from_user.id] = {'words': words.copy()}
    button_1 = KeyboardButton(text='Начать')
    button_2 = KeyboardButton(text='/help')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button_1, button_2]], resize_keyboard=True, one_time_keyboard=True)
    await message.answer(
    'Привет 👋 Давай попрактикуемся в английском языке. ' 
    'Тренировки можешь проходить в удобном для себя темпе.',
    reply_markup=keyboard
)

# Этот хэндлер будет срабатывать на команду "/help"
# @dp.message(Command(commands='help'))
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

# Этот хэндлер будет срабатывать на кнопку "начать"
# @dp.message(F.text.lower().in_(['начать', 'дальше ⏭']))
async def process_start_words(message: Message, state: FSMContext):
    word = choice(users[message.from_user.id]['words'])
    # users[message.from_user.id]['current_word'] = word
    await state.set_state(CheckTranslate.tr_word)
    await state.update_data(tr_word=word)
    var_buttons = [
        word['tr'], word['var_1'], word['var_2'], word['var_3']
    ]
    builder = keyboard_builder(var_buttons)
    await state.set_state(CheckTranslate.var)
    await message.answer(
        f'Выбери перевод слова:\n"{word["word"]}"',
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
    )


# @dp.message(StateFilter(CheckTranslate.var))
async def process_check_translate(message: Message, state: FSMContext):
    # word = users[message.from_user.id]['current_word']
    await state.update_data(var=message.text)
    data = await state.get_data()
    word = data.get('tr_word')
    print(word)
    if message.text.lower() == word['tr'].lower():
        builder = main_buttons()
        answer = ['Правильно!', 'Совершенно верно!', 'Точно!', 'Отлично!', 'Прекрасно!']
        await state.clear()
        await message.answer(
            f'{choice(answer)} Продолжаем?', 
            reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
        )
    else:
        var_buttons = [
        word['tr'], word['var_1'], word['var_2'], word['var_3']
    ]
        builder = keyboard_builder(var_buttons)
        answer = ['Неверный ответ', 'Неправильный ответ', 'Неправильно']
        await state.set_state(CheckTranslate.var)
        await message.answer(
            f'{choice(answer)}, попробуйте еще раз\n'
            f'Слово "{word["word"]}"',
            reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
        )

# @dp.message(F.text.lower().in_(['удалить слово 🔙', 'удалить слово']))
async def delete_word(message: Message, state: FSMContext):
    builder = ReplyKeyboardBuilder().add(KeyboardButton(text='/cancel'))
    await message.answer(
        'Введите слово на русском 🇷🇺 которое нужно удалить '
        'или нажмите /cancel если передумали',
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
    )
    await state.set_state(WordToDelete.word_to_del)


# @dp.message(F.text.lower().in_(['добавить слово ➕', 'добавить слово', 'продолжить добавление']))
async def process_word_fillform(message: Message, state: FSMContext):
    builder = ReplyKeyboardBuilder().add(KeyboardButton(text='/cancel'))
    await message.answer(
        text='Введите слово на русском 🇷🇺\n'
        'Или нажмите /cancel для отмены',
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
    )
    await state.set_state(AddWordForm.word)

# @dp.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel(message: Message, state: FSMContext):
    builder = ReplyKeyboardBuilder().add(KeyboardButton(text='Дальше ⏭'))
    await message.answer(
        text='Вы отменили процесс добавления слова\n'
             'Чтобы вернуться к изучению слов, '
             'нажмите "Дальше ⏭"',
             reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
    )
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()

async def process_word_delete(message: Message, state: FSMContext):
    word_to_del = message.text
    try:
        for w in users[message.from_user.id]['words']:
            if word_to_del.lower() == w['word'].lower():
                users[message.from_user.id]['words'].remove(w)
        await state.clear()
        builder = ReplyKeyboardBuilder().add(KeyboardButton(text='Дальше ⏭'))
        await message.answer(
            text='Слово удалено ❌ Продолжаем?',
            reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
        )
    except:
        await state.clear()
        builder = ReplyKeyboardBuilder().add(KeyboardButton(text='Дальше ⏭'))
        await message.answer(
            text='Слово не найдено!\n'
            'Нажмите дальше ⏭, чтобы продолжить тренинг',
            reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
        )

# @dp.message(StateFilter(AddWordForm.word))
async def process_word_sent(message: Message, state: FSMContext):
    builder = ReplyKeyboardBuilder().add(KeyboardButton(text='/cancel'))
    await state.update_data(word=message.text)
    await message.answer(
        text='Теперь введите правильный перевод слова на английском 🇬🇧',
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
    )
    await state.set_state(AddWordForm.tr)

# @dp.message(StateFilter(AddWordForm.tr))
async def process_tr_sent(message: Message, state: FSMContext):
    builder = ReplyKeyboardBuilder().add(KeyboardButton(text='/cancel'))
    await state.update_data(tr=message.text)
    await message.answer(
        text='Введите первый вариант неправильного перевода на английский',
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
    )
    await state.set_state(AddWordForm.var_1)

# @dp.message(StateFilter(AddWordForm.var_1))
async def process_var_1_sent(message: Message, state: FSMContext):
    builder = ReplyKeyboardBuilder().add(KeyboardButton(text='/cancel'))
    await state.update_data(var_1=message.text)
    await message.answer(
        text='Введите второй вариант неправильного перевода на английский',
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
    )
    await state.set_state(AddWordForm.var_2)

# @dp.message(StateFilter(AddWordForm.var_2))
async def process_var_2_sent(message: Message, state: FSMContext):
    builder = ReplyKeyboardBuilder().add(KeyboardButton(text='/cancel'))
    await state.update_data(var_2=message.text)
    await message.answer(
        text='Введите третий вариант неправильного перевода на английский',
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
    )
    await state.set_state(AddWordForm.var_3)

# @dp.message(StateFilter(AddWordForm.var_3))
async def process_var_3_sent(message: Message, state: FSMContext):
    builder = ReplyKeyboardBuilder().add(KeyboardButton(text='Дальше ⏭'))
    await state.update_data(var_3=message.text)
    users[message.from_user.id]['words'].extend(await state.get_data())
    await state.clear()
    await message.answer(
        text='Спасибо! Новое слово добавлено. '
        'Чтобы вернуться к изучению слов, '
        'нажмите "Дальше ⏭"',
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
    )

# @dp.message()
async def other_messages(message: Message):
    builder = ReplyKeyboardBuilder().add(KeyboardButton(text='Начать'))
    await message.answer(
        'Не знаю такой команды.\n'
        'Нажмите "Начать", чтобы запустить тренажер',
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
    )

dp.message.register(process_start_command, CommandStart())
dp.message.register(process_help_command, Command(commands='help'))
dp.message.register(process_start_words, F.text.lower().in_(['начать', 'дальше ⏭']))
dp.message.register(delete_word, F.text.lower().in_(['удалить слово 🔙', 'удалить слово']))
dp.message.register(process_word_fillform, F.text.lower().in_(['добавить слово ➕', 'добавить слово']))
dp.message.register(process_check_translate, StateFilter(CheckTranslate.var))
dp.message.register(process_cancel, Command(commands='cancel'), ~StateFilter(default_state))
dp.message.register(process_word_delete, StateFilter(WordToDelete.word_to_del))
dp.message.register(process_word_sent, StateFilter(AddWordForm.word))
dp.message.register(process_tr_sent, StateFilter(AddWordForm.tr))
dp.message.register(process_var_1_sent, StateFilter(AddWordForm.var_1))
dp.message.register(process_var_2_sent, StateFilter(AddWordForm.var_2))
dp.message.register(process_var_3_sent, StateFilter(AddWordForm.var_3))
dp.message.register(other_messages)


if __name__ == '__main__':
    dp.run_polling(bot)