from aiogram import types

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
