from random import shuffle

from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

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