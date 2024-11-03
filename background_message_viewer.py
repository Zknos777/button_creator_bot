from aiogram import Bot
from datetime import datetime, timedelta
import asyncio, psycopg2
from aiogram.client.session.aiohttp import AiohttpSession
from utils import get_keyboard

TOKEN = "6303536387:AAGctZGRKGqn-4-M8ww0yzUYnyNp079XOSY"
admin_id = 1233498701            ## ID admin
first_group_id =  -1002491824558 #-1002098393146  ## ID first group
second_group_id = -1002400799616 #-1001520768042 ## ID second group
#TOKEN = "7411995656:AAGqJW5nYm8iDMhd-iQOd0WdK1Si3Auk79Q" ##Real Token!

session = AiohttpSession()
bot = Bot(token=TOKEN, session=session)


async def main():
    connection = psycopg2.connect(database="posts",
                                  host="localhost",
                                  user="username",
                                  password="password",
                                  port=5432)

    cursor = connection.cursor()
    while True:
        cursor.execute("SELECT * from Posts")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
            column_names = [desc[0] for desc in cursor.description]
            data = dict(zip(column_names, row))
            dt_posted = datetime.strptime(data["datetime_posted"][:19], "%Y-%m-%d %H:%M:%S")
            dt_to_delete = datetime.strptime(data["datetime_to_delete"][:19], "%Y-%m-%d %H:%M:%S")
            header, text = data["msg_text"].split("\n")
            # print(data)
            # print(data['id'])

            ## Если настало время удаление и прошло более 2 суток
            if abs((dt_to_delete - dt_posted)) >= timedelta(seconds=2):
                await bot.send_message(5782652783, f'ПОРА УДАЛИТЬ СООБЩЕНИЕ! ID = {row[0]}')
                await bot.send_message(5782652783, f'https://t.me/TestKaras1/{data['msg_id']}')
                await bot.send_message(text=f'{header}',
                                       reply_markup=get_keyboard(data["button_text"], data["button_link"]),
                                       chat_id=second_group_id)
                try:
                    delete_query = "DELETE FROM Posts WHERE id = %s"
                    cursor.execute(delete_query, (data['id'],))
                    #cursor.execute(f"DELETE FROM Posts WHERE id = {data['id']}")
                    connection.commit()
                except Exception as e:
                    print(e)
                    connection = psycopg2.connect(database="posts",
                                                  host="localhost",
                                                  user="username",
                                                  password="password",
                                                  port=5432)

                    cursor = connection.cursor()
                #connection.commit()
                await session.close()
            ## Если настало время удаление
            elif dt_to_delete <= datetime.today():
                await bot.send_message(5782652783, f'"Тут удаляем СООБЩЕНИЕ автоматически и постим новое! {row[0]}"')
                await bot.send_message(5782652783, "Сессия закрыта!")
                await bot.send_message(text=f'{header}',
                                       reply_markup=get_keyboard(data["button_text"], data["button_link"]),
                                       chat_id=second_group_id)
                try:
                    delete_query = "DELETE FROM Posts WHERE id = %s"
                    cursor.execute(delete_query, (data['id'],))
                    # cursor.execute(f"DELETE FROM Posts WHERE id = {data['id']}")
                    #connection.commit()
                except Exception as e:
                    print(e.message)
                    connection = psycopg2.connect(database="posts",
                                                  host="localhost",
                                                  user="username",
                                                  password="password",
                                                  port=5432)

                    #cursor = connection.cursor()
                await session.close()
            #else:
                #await bot.send_message(5782652783, "Нет сообщений дял удаления")
                #await bot.send_message(5782652783, "Сессия закрыта!")
                #await session.close()

            await asyncio.sleep(10)



if __name__ == "__main__":
    asyncio.run(main())