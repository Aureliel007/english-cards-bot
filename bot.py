from configparser import ConfigParser

from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram import F

from handlers import *


# Вместо BOT TOKEN HERE нужно вставить токен вашего бота, полученный у @BotFather
config = ConfigParser()
config.read('config.ini')
BOT_TOKEN = config['TGBot']['token']

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.message.register(process_start_command, CommandStart())
dp.message.register(process_help_command, Command(commands='help'))
dp.message.register(process_start_words, F.text.lower().in_(['начать', 'дальше ⏭']))
dp.message.register(delete_word, F.text.lower().in_(['удалить слово 🔙', 'удалить слово']))
dp.message.register(process_word_fillform, F.text.lower().in_(['добавить слово ➕', 'добавить слово']))
dp.message.register(process_check_translate, StateFilter(CheckTranslate.var))
dp.message.register(process_cancel, Command(commands='cancel'), ~StateFilter(default_state))
dp.message.register(process_word_delete, StateFilter(WordToDelete.word_to_del))
dp.message.register(process_word_sent, StateFilter(AddWordForm.rus))
dp.message.register(process_translate_sent, StateFilter(AddWordForm.eng))
dp.message.register(other_messages)


if __name__ == '__main__':
    dp.run_polling(bot)
