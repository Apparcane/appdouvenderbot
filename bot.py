import config
import logging
import asyncio
from ongoing import *
from datetime import datetime

from aiogram import Bot, Dispatcher, executor, types
from sqlighter import SQLighter
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from stopgame import StopGame

from contextvars import ContextVar

# chat_id
chat_id = ContextVar('id', default=650147497)

# задаем уровень логов
logging.basicConfig(level=logging.INFO)

# инициализируем бота
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# инициализируем соединение с БД
db = SQLighter('db.db')

# инициализируем парсер
sg = StopGame('lastkey.txt')


# start
@dp.message_handler(commands=['start'])
async def subscribe(message: types.Message):
    print("Id: " + str(message.from_user.id) + "\nFirst Name: " +
          str(message.from_user.username) + "\nText: " + str(message.text) + "\n")
    chat_id.set(message.from_user.id)
    me = await bot.get_me()
    await message.answer(f'Привет, меня зовут {me.first_name}. Я пока что в разработке, так что не ожидай много-го 😀')


@dp.message_handler(commands=['news'])
async def news(message: types.Message):
    try:
        await message.answer("Одну секунду ...")

        answer = ''
        clock = 0

        for i in ongoing_all(1):
            answer = str(answer) + str(i) + str('\n')
            clock = clock + 1
            if clock % 11 == 0:
                await message.answer(answer)
                clock = 1
                answer = ''
                await message.answer(answer)

    except Exception as e:
        print(repr(e))

# Команда активации подписки
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    print("Id: " + str(message.from_user.id) + "\nFirst Name: " +
          str(message.from_user.username) + "\nText: " + str(message.text) + "\n")
    if(not db.subscriber_exists(message.from_user.id)):
        # если юзера нет в базе, добавляем его
        db.add_subscriber(message.from_user.username, message.from_user.id)
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        db.update_subscription(message.from_user.username,
                               message.from_user.id, True)

    await message.answer("Вы успешно подписались на рассылку!\nЖдите, скоро выйдут новые обзоры и вы узнаете о них первыми =)")


# Команда отписки
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    print("Id: " + str(message.from_user.id) + "\nFirst Name: " +
          str(message.from_user.username) + "\nText: " + str(message.text) + "\n")
    if(not db.subscriber_exists(message.from_user.id)):
        # если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
        db.add_subscriber(message.from_user.username,
                          message.from_user.id, False)
        await message.answer("Вы итак не подписаны.")
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        db.update_subscription(message.from_user.username,
                               message.from_user.id, False)
        await message.answer("Вы успешно отписаны от рассылки.")


# Сама рассылка
# async def scheduled(wait_for):
#     id = chat_id.get()
#     while True:
#         await asyncio.sleep(wait_for)

#         # провераем наличие новых игр
#         new_games = sg.new_games()

#         if(new_games):
#             # если игры есть, переворачиваем список и итерируем
#             new_games.reverse()

#             for ng in new_games:
#                 nfo = sg.game_info(ng)

#                 # получаем список подписчиков бота
#                 subscriptions = db.get_subscriptions()

#                 # отправляем всем новость
#                 with open(sg.download_image(nfo['image']), 'rb') as photo:
#                     for s in subscriptions:
#                         await bot.send_photo(s[0], photo, caption=nfo['title'] + "\n" + "Оценка: " + nfo['score'] + "\n" + nfo['excerpt'] + "\n\n" + nfo['link'], disable_notification=True)

#                 # обновляем ключ
#                 sg.update_lastkey(nfo['id'])


# Просто разговор
@dp.message_handler(content_types=['text'])
async def talk(message: types.Message):
    print("Id: " + str(message.from_user.id) + "\nFirst Name: " +
          str(message.from_user.username) + "\nText: " + str(message.text) + "\n")
    await message.answer(message.from_user.username)


# запускаем лонг поллинг
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # loop.create_task(scheduled(10))  # 10 секунд
    executor.start_polling(dp, skip_updates=True)