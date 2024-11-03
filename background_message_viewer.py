from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from datetime import datetime
import asyncio
from aiogram.client.session.aiohttp import AiohttpSession


TOKEN = "6303536387:AAGctZGRKGqn-4-M8ww0yzUYnyNp079XOSY"
admin_id = 1233498701            ## ID admin
first_group_id =  -1002491824558 #-1002098393146  ## ID first group
second_group_id = -1002400799616 #-1001520768042 ## ID second group
#TOKEN = "7411995656:AAGqJW5nYm8iDMhd-iQOd0WdK1Si3Auk79Q" ##Real Token!

session = AiohttpSession()
bot = Bot(token=TOKEN, session=session)

import psycopg2

connection = psycopg2.connect(database="posts",
                        host="localhost",
                        user="username",
                        password="password",
                        port=5432)



async def main():
    cursor = connection.cursor()
    cursor.execute("SELECT * from Posts")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    for row in rows:
        # print(row)
        # print(datetime.strptime(row[-1], "%Y-%m-%d %H:%M:%S"))
        if (datetime.strptime(row[-1], "%Y-%m-%d %H:%M:%S")) <= datetime.today():
            await bot.send_message(5782652783, f'"ПОРА УДАЛИТЬ СООБЩЕНИЕ! {row[0]}"')
            await bot.send_message(5782652783, "Сессия закрыта!")
            await session.close()
        else:
            await bot.send_message(5782652783, "Нет сообщений дял удаления")
            await bot.send_message(5782652783, "Сессия закрыта!")
            await session.close()



if __name__ == "__main__":
    asyncio.run(main())