from configparser import ConfigParser

from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram import F

import handlers


# Вместо BOT TOKEN HERE нужно вставить токен вашего бота, полученный у @BotFather
config = ConfigParser()
config.read('config.ini')
BOT_TOKEN = config['TGBot']['token']

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.message.register(handlers.process_start_command, CommandStart())
dp.message.register(handlers.process_help_command, Command(commands='help'))
dp.message.register(handlers.process_start_words, F.text.lower().in_(['начать', 'дальше ⏭']))
dp.message.register(handlers.delete_word, F.text.lower().in_(['удалить слово 🔙', 'удалить слово']))
dp.message.register(handlers.process_word_fillform, F.text.lower().in_(['добавить слово ➕', 'добавить слово']))
dp.message.register(handlers.process_check_translate, StateFilter(handlers.CheckTranslate.var))
dp.message.register(handlers.process_cancel, Command(commands='cancel'), ~StateFilter(default_state))
dp.message.register(handlers.process_word_delete, StateFilter(handlers.WordToDelete.word_to_del))
dp.message.register(handlers.process_word_sent, StateFilter(handlers.AddWordForm.word))
dp.message.register(handlers.process_tr_sent, StateFilter(handlers.AddWordForm.tr))
dp.message.register(handlers.process_var_1_sent, StateFilter(handlers.AddWordForm.var_1))
dp.message.register(handlers.process_var_2_sent, StateFilter(handlers.AddWordForm.var_2))
dp.message.register(handlers.process_var_3_sent, StateFilter(handlers.AddWordForm.var_3))
dp.message.register(handlers.other_messages)


if __name__ == '__main__':
    dp.run_polling(bot)
