import asyncio, logging, sys
from config import BOT_TOKEN

from aiogram import Bot, Dispatcher, html, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message


headers = {1: "Shapochka 1",
           2: "Shapochka 2 gde est odin i tot je text!",
           3: "Shapochka 3 gde toje est odin i tot je text!"}


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
    await message.answer("Привет. Выбери шапку сообщений!")


@dp.message(Form.header)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(header=message.text)
    await state.set_state(Form.text)
    await message.answer(
        f"Отлично, {html.quote(message.text)}!\nКакой текст соообщения?",
    )

@dp.message(Form.text)
async def process_like_write_bots(message: Message, state: FSMContext) -> None:
    await state.update_data(text=message.text)
    await state.set_state(Form.link_text)
    await message.reply("Текст ссылки?")


@dp.message(Form.link_text)
async def process_like_write_bots(message: Message, state: FSMContext) -> None:
    await state.update_data(link_text=message.text)
    await state.set_state(Form.link_url)
    await message.reply("Линк ссылки?")


@dp.message(Form.link_url)
async def process_like_write_bots(message: Message, state: FSMContext) -> None:
    await state.update_data(link_url=message.text)
    await state.set_state(Form.link_url)
    await message.reply("Готово всё!")
    data = await state.get_data()
    await message.answer(f'{headers[int(data["header"])]}\n{data["text"]}',
                         reply_markup = get_keyboard(data["link_text"], data["link_url"]))
    await state.clear()
    ###постинг и автоудаление
    name_group = -1002182879621 ## ID group
    msg = await bot.send_message(text=f'{headers[int(data["header"])]}\n{data["text"]}',
                         reply_markup = get_keyboard(data["link_text"], data["link_url"]), chat_id=name_group)
    await message.answer("1")
    await asyncio.sleep(20) ## timeout of delete message
    await msg.delete() ### удаляет сообщение


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())