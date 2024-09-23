import asyncio, json, logging, sys
from builtins import str
from os import getenv
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import Bot, Dispatcher, html, types
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message
from utils import kb_create, get_keyboard

TOKEN = "7411995656:AAGqJW5nYm8iDMhd-iQOd0WdK1Si3Auk79Q"

dp = Dispatcher()
with open('headers.json', 'r') as fp:
    headers = json.load(fp)


class Form(StatesGroup):
    choose_header = State()
    text = State()
    finish = State()
    link_url = State()
    timer = State()
    edit_new_text = State()
    edit_new_link = State()
    header_del = State()
    edit_new_number = State()


@dp.message(Command("edit")) ## Изменние шапки и текста
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


@dp.message(Command("del"))
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



@dp.message(Command("edit")) ## Изменние шапки и текста
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


#@dp.message(Command("stop"), state="*")
@dp.message(Command("stop"), ~StateFilter(default_state))
async def stop(message: Message, state: FSMContext):
    await message.answer("Остановлено!", reply_markup=types.ReplyKeyboardRemove())
    await state.clear()


@dp.message(CommandStart())
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
    await state.update_data(header=message.text)
    await message.answer(
        f"Отлично, {html.quote(message.text)}!\nКакой текст соообщения?",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(Form.link_url)


@dp.message(Form.link_url)
async def process_like_write_bots(message: Message, state: FSMContext) -> None:
    await state.update_data(text=message.text)
    await message.reply("Укажите адресс ссылки")
    await state.set_state(Form.timer)


@dp.message(Form.timer)
async def process_like_write_bots(message: Message, state: FSMContext) -> None:
    await state.update_data(link_url=message.text)
    await message.reply("Через сколько минут удалять сообщение?")
    await state.set_state(Form.finish)


@dp.message(Form.finish)
async def process_like_write_bots(message: Message, state: FSMContext, bot=Bot) -> None:
    await state.update_data(timer=message.text)
    await message.reply("Готово всё!")
    data = await state.get_data()
    await message.answer(f'{headers[str(data["header"])][0]}\n{data["text"]}',
                         reply_markup = get_keyboard(headers[str(data["header"])][1], data["link_url"]))
    ###постинг и автоудаление
    name_group = -1002098393146 ## ID first group
    msg = await bot.send_message(text=f'{headers[str(data["header"])][0]}\n{data["text"]}',
                                reply_markup = get_keyboard(headers[str(data["header"])][1], data["link_url"]),
                                chat_id=name_group)

    await asyncio.sleep(int(data["timer"])*60) ## timeout of delete message
    if int(data["timer"])*60 < 7200:
        await msg.delete() ### удаляет сообщение
    else:
        ## Если более 48 часов то пишет сообщение о том, что нужно удалить сообщение
        await bot.send_message(text=f"Удали сообщение! https://t.me/c/{str(msg.chat.id)[4:]}/{msg.message_id}",
                               chat_id=1233498701)
    ##posting second group
    await bot.send_message(text=f'{headers[str(data["header"])][0]}\n{data["text"]}',
                                 reply_markup=get_keyboard(headers[str(data["header"])][1], data["link_url"]),
                                 chat_id=-1001520768042)

    await state.clear()
    
async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())