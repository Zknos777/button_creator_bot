import asyncio, logging, sys
from config import BOT_TOKEN
from utils import kb_create
from aiogram import Bot, Dispatcher, html, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder


headers = {1: ("Shapochka 1", "Text_knopki1"),
           2: ("Shapochka 2 gde est odin i tot je text!", "Text_knopki2"),
           3: ("Shapochka 3 gde toje est odin i tot je text!", "Text_knopki3"),
           4: ("Shapochka 4", "Text_knopki4"),
           5: ("Shapochka 5 gde est odin i tot je text!", "Text_knopki5"),
           6: ("Shapochka 6 gde toje est odin i tot je text!", "Text_knopki6"),
           7: ("Shapochka 7", "Text_knopki7"),
           8: ("Shapochka 8 gde est odin i tot je text!", "Text_knopki8"),
           9: ("Shapochka 9 gde toje est odin i tot je text!", "Text_knopki9"),
           10: ("Shapochka 10", "Text_knopki10"),
           11: ("Shapochka 11 gde est odin i tot je text!", "Text_knopki11"),
           12: ("Shapochka 12 gde toje est odin i tot je text!", "Text_knopki12")
           }


def get_keyboard(text_button, link_button):
    buttons = [types.InlineKeyboardButton(text=text_button, url=link_button)],
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

class Form(StatesGroup):
    header = State()
    text = State()
    link_text = State()
    link_url = State()

dp = Dispatcher()
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

@dp.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.header)
    builder = ReplyKeyboardBuilder()
    for key in list(headers.keys()): ## Все кнопки из ключей в словаре
        builder.add(types.KeyboardButton(text=str(key)))
    builder.adjust(4) #делаем по 4 кнопки на строку
    await message.answer(
        "Привет. Выбери шапку сообщений!",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )


@dp.message(Form.header)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(header=message.text)
    await state.set_state(Form.link_text)
    await message.answer(
        f"Отлично, {html.quote(message.text)}!\nКакой текст соообщения?",
        reply_markup=types.ReplyKeyboardRemove()
    )


@dp.message(Form.link_text)
async def process_like_write_bots(message: Message, state: FSMContext) -> None:
    await state.update_data(text=message.text)
    await state.set_state(Form.link_url)
    await message.reply("Линк ссылки?")


@dp.message(Form.link_url)
async def process_like_write_bots(message: Message, state: FSMContext) -> None:
    await state.update_data(link_url=message.text)
    await state.set_state(Form.link_url)
    await message.reply("Готово всё!")
    data = await state.get_data()
    await message.answer(f'{headers[int(data["header"])][0]}\n{data["text"]}',
                         reply_markup = get_keyboard(headers[int(data["header"])][1], data["link_url"]))
    await state.clear()
    ###постинг и автоудаление
    name_group = -1002182879621 ## ID group
    msg = await bot.send_message(text=f'{headers[int(data["header"])][0]}\n{data["text"]}',
                         reply_markup = get_keyboard(headers[int(data["header"])][1], data["link_url"]), chat_id=name_group)
    await message.answer("1")
    await asyncio.sleep(20) ## timeout of delete message
    await msg.delete() ### удаляет сообщение


@dp.message(Command("Headers", "headers"))
async def show_headers(message: Message):
    for k,v in headers.items():
        await message.answer(f'{k} - {v}', reply_markup=get_keyboard("Изменить шапку",
                                                                     "http://google.ru"))
    await message.answer(reply_markup=kb_create("Создать новую", "Удалить"))


@dp.message(F.Text == "удалить")
async def delete_header(message: Message):
    await message.answer("Какую шапку удалить?")


@dp.message(F.Text.lower() == "создать новую")
async def create_header(message: Message):
    await message.answer("Введите текст новой шапки")


# @dp.message(Command("Edit", "edit"))
# async def show_headers(message: Message):
#     await message.answer(f'{k} - {v}')


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())