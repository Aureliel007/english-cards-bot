from aiogram.fsm.state import State, StatesGroup

class AddWordForm(StatesGroup):
    rus = State()
    eng = State()

class CheckTranslate(StatesGroup):
    tr_word = State()
    var = State()

class WordToDelete(StatesGroup):
    word_to_del = State()
