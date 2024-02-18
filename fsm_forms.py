from aiogram.fsm.state import State, StatesGroup

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