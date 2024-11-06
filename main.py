import asyncio, json, logging, sys
from datetime import datetime
from builtins import str
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message
from utils import *
import psycopg2

connection = psycopg2.connect(database="posts",
                        host="localhost",
                        user="username",
                        password="password",
                        port=5432)


cursor = connection.cursor()
# cursor.execute("DROP TABLE Posts") ## очищаем таблицу
# connection.commit()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Posts (
id SERIAL PRIMARY KEY,
msg_text TEXT NOT NULL,
msg_id TEXT NOT NULL,
msg_chat_id TEXT NOT NULL,
button_text TEXT NOT NULL,
button_link TEXT NOT NULL,
datetime_posted TEXT NOT NULL,
datetime_to_delete TEXT NOT NULL
)
''')

# Сохраняем изменения
connection.commit()


#TOKEN = "6303536387:AAGctZGRKGqn-4-M8ww0yzUYnyNp079XOSY" ##TEST token
#first_group_id =  -1002491824558                         ## TEST ID first group
#second_group_id = -1002400799616                         ## TEST ID second group
admin_id = 1233498701            ## ID admin

first_group_id =  -1002098393146                         ##REAL ID first group
second_group_id = -1001520768042                         ##REAL ID second group
TOKEN = "7411995656:AAGqJW5nYm8iDMhd-iQOd0WdK1Si3Auk79Q" ##REAL Token!

dp = Dispatcher()
with open('headers.json', 'r') as fp:
    headers = json.load(fp)

############ DELETE HEADER #########
@dp.message(F.from_user.id.in_({5782652783, 1233498701}), Command("del"))
async def delete_header(message: Message, state: FSMContext):
    builder = ReplyKeyboardBuilder()
    for key in list(headers.keys()):  ## Все кнопки из ключей в словаре
        builder.add(types.KeyboardButton(text=str(key)))
    builder.adjust(4)  # делаем по 4 кнопки на строку
    await message.answer("Выбери шапку сообщений для удаления!!",
        reply_markup=builder.as_markup(resize_keyboard=True),)
    await state.set_state(Form.header_del)


@dp.message(Form.header_del)
async def delete_header_handler(message: Message, state: FSMContext) -> None:
    if message.text in headers.keys():
        del headers[str(message.text)]
        await state.clear()
        await message.answer(f"Шапка {message.text} удалена!", reply_markup=types.ReplyKeyboardRemove())
        with open('headers.json', 'w') as fp:
            json.dump(headers, fp, indent=6)
    else:
        await message.answer("Не смог удалить! Попробуйте ещё раз", reply_markup=types.ReplyKeyboardRemove())
        await state.clear()


############ EDIT HEADER #########
@dp.message(F.from_user.id.in_({5782652783, 1233498701}), Command("edit")) ## Изменние шапки и текста
async def edit_header(message: Message, state: FSMContext):
    builder = ReplyKeyboardBuilder()
    for key in list(headers.keys()):  ## Все кнопки из ключей в словаре
        builder.add(types.KeyboardButton(text=str(key)))
    builder.adjust(4)  # делаем по 4 кнопки на строку
    await message.answer(
        "Выбери шапку сообщений для изменения!",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )
    await state.set_state(Form.edit_new_number)

@dp.message(Form.edit_new_number)
async def edit_header_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(edit_new_number=message.text)
    await message.reply("Укажите новый текст шапки")
    await state.set_state(Form.edit_new_text)


@dp.message(Form.edit_new_text)
async def edit_header_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(edit_new_text=message.text)
    await message.reply("Укажите новый текст кнопки")
    await state.set_state(Form.edit_new_link)


@dp.message(Form.edit_new_link)
async def edit_header_handler(message: Message, state: FSMContext) -> None:
        await state.update_data(edit_new_link=message.text)
        await state.set_state(Form.edit_new_link)
        data = await state.get_data()
        headers[str(data["edit_new_number"])] = (data["edit_new_text"], data["edit_new_link"]) ## изменение словаря
        with open('headers.json', 'w') as fp: ## запись словаря
            json.dump(headers, fp, indent=6)
        await message.answer("Шапка успешно изменена!", reply_markup=types.ReplyKeyboardRemove())
        await state.clear()
        print(headers.items())


############ STOP COMMAND #########
@dp.message(F.from_user.id.in_({5782652783, 1233498701}), Command("stop"), ~StateFilter(default_state))
async def stop(message: Message, state: FSMContext):
    await message.answer("Остановлено!", reply_markup=types.ReplyKeyboardRemove())
    await state.clear()


############ START COMMAND #########
@dp.message(F.from_user.id.in_({5782652783, 1233498701}), CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")
    builder = ReplyKeyboardBuilder()
    for key in list(headers.keys()): ## Все кнопки из ключей в словаре
        builder.add(types.KeyboardButton(text=str(key)))
    builder.adjust(4) #делаем по 4 кнопки на строку
    await message.answer(
        "Привет. Выбери шапку сообщений!",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )
    await state.set_state(Form.text)


@dp.message(Form.text)
async def process_name(message: Message, state: FSMContext) -> None:
    ##Проверка на правильность выбора шапки
    if not message.text in list(headers.keys()):
        await message.answer("Выберите шапку из предложенных!")
        return

    await state.update_data(header=message.text) ## записываем в память выбранную шапку
    await message.answer(
            f"Отлично, {html.quote(message.text)}!\nУкажите текст соообщения?",
            reply_markup=types.ReplyKeyboardRemove()
            )
    await state.set_state(Form.link_url)


@dp.message(Form.link_url)
async def process_like_write_bots(message: Message, state: FSMContext) -> None:
    await state.update_data(text=message.text)
    await message.reply("Укажите адрес ссылки?")
    await state.set_state(Form.detele_datetime)


@dp.message(Form.detele_datetime)
async def process_like_write_bots(message: Message, state: FSMContext) -> None:
    await state.update_data(link_url=message.text)
    await message.reply("Укажите дату и время удаление в формате 21.10.2024 16:59?")
    await state.set_state(Form.finish)


@dp.message(Form.finish)
async def process_like_write_bots(message: Message, state: FSMContext, bot=Bot) -> None:
    ##Проверка на правильность даты
    if not datetime.strptime(message.text, "%d.%m.%Y %H:%M") >= datetime.today():
        await message.answer("Указанная дата имеет неправильный формат!")
        return

    await state.update_data(detele_datetime=message.text)
    await message.reply("Готово всё!")
    data = await state.get_data()
    await message.answer(f'{headers[str(data["header"])][0]}\n{data["text"]}',
                         reply_markup = get_keyboard(headers[str(data["header"])][1], data["link_url"]))
    ###постинг и автоудаление
    msg = await bot.send_message(text=f'{headers[str(data["header"])][0]}\n{data["text"]}',
                                reply_markup = get_keyboard(headers[str(data["header"])][1], data["link_url"]),
                                chat_id=first_group_id)
    msg_text, msg_id, msg_chat_id, button_text, button_link = (msg.text, msg.message_id, str(msg.chat.id)[1:],
                                                               msg.reply_markup.inline_keyboard[0][0].text,
                                                               msg.reply_markup.inline_keyboard[0][0].url)
    print(msg_text, msg_id, msg_chat_id, button_text, button_link)
    date_to_delete = datetime.strptime(str(data["detele_datetime"]), "%d.%m.%Y %H:%M")
    #Записываем все данные этого сообщения в БД
    cursor.execute('INSERT INTO Posts (msg_text, msg_id, msg_chat_id, button_text, button_link, datetime_posted, datetime_to_delete) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                   (msg_text, msg_id, msg_chat_id, button_text, button_link, str(msg.date), str(date_to_delete)))
    connection.commit()
    await state.clear()
    
async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())