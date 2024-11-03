from aiogram import types
from aiogram.fsm.state import State, StatesGroup

def kb_create(*args):
    kb = [
        [
            types.KeyboardButton(text=args[0]),
            types.KeyboardButton(text=args[1])
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите способ подачи"
    )
    return keyboard


def get_keyboard(text_button, link_button):
    buttons = [types.InlineKeyboardButton(text=text_button, url=link_button)],
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

class Form(StatesGroup):
    choose_header = State()
    text = State()
    text_check = State()
    finish = State()
    link_url = State()
    detele_datetime = State()
    edit_new_text = State()
    edit_new_link = State()
    header_del = State()
    edit_new_number = State()