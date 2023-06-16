# -*- coding: utf-8 -*-
import os
from aiogram import Bot, Dispatcher, executor, types
import time

API_TOKEN = '6245533640:AAFa5p1awQe4H0tQhoi7TEQxHPgX993P69E'

botQuest = Bot(token=API_TOKEN)
dp = Dispatcher(botQuest)
story_wait = False
now_w = False
story_name = ''

@dp.message_handler(commands=['start'])  # Явно указываем в декораторе, на какую команду реагируем.
async def send_welcome(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Я хочу создать свой собственную историю!", callback_data='ready_tw')],
        [types.KeyboardButton(text="Я хочу прочесть истории других людей!", callback_data='ready_tr')]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    welcome_message = f"Приветствую тебя, поэт-путник, в мире стихов и рифм! \n Я твой верный помощник, бот, " \
                      f"но душа у меня жива. \n Записывать и читать стихи - вот мое призвание, \n С радостью я помогу "\
                      f"воплотить в них твое вдохновение. "
    await message.reply(welcome_message, reply_markup=keyboard)  # Так как код работает асинхронно, то обязательно
    # пишем await.


@dp.message_handler()  # Создаём новое событие, которое запускается в ответ на любой текст, введённый пользователем.
async def communicate(message: types.Message):
    callback_data = message.text

    global story_wait
    global now_w
    global story_name

    if story_wait:
        story_name = callback_data
        story_wait = False

    if callback_data == "Начнём запись":
        now_w = True
        story_wait = True

    if callback_data == "Конец.":
        now_w = False

    if (callback_data + '.txt') in os.listdir("data") and not now_w:
        try:
            await message.answer("Я начинаю рассказ...")
            time.sleep(2)
            with open(f'data/{callback_data}.txt', 'r', encoding='UTF-8') as f:
                lines = f.read().split('\n')
                for line in lines:
                    # print(line)
                    await message.answer(line.replace("%n%", "\n"))
                    delay = len(line) * 0.08
                    time.sleep(delay)
        except FileNotFoundError:
            await message.reply("Файл не найден")

    else:
         if callback_data == "Начнём запись":
        await message.reply(text="Хорошо, начнём! Сначала название, потом всё остальное.",
                            reply_markup=types.ReplyKeyboardRemove())

    elif callback_data == "Я хочу создать свой собственную историю!":
        await message.reply(text="Отлично. Подтверди свой выбор!", reply_markup=types.ReplyKeyboardRemove())
        kb = [
            [types.KeyboardButton(text="Начнём запись", callback_data='writing')],
            [types.KeyboardButton(text="Я передумал - не нужно начинать запись", callback_data='ready_tr')]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.reply("...", reply_markup=keyboard)

    elif callback_data in ["Я хочу прочесть истории других людей!", "Список"]:
        await message.reply("Вот список")
        stories = os.listdir("data")
        for story in stories:
            await message.answer(story.replace("%n%", "\n")[:-4])
            delay = len(story) * 0.08
            time.sleep(delay)

    elif callback_data == "Я передумал - не нужно начинать запись":
        await message.reply("Хорошо. Я не настаиваю", reply_markup=types.ReplyKeyboardRemove())

    elif callback_data == "Конец.":
        await message.reply("Запись завершена", reply_markup=types.ReplyKeyboardRemove())

    else:
        # Если флаг записи включен, то записываем сообщение.
        if now_w:
            with open(f'data/{story_name}.txt', 'a', encoding='UTF-8') as f:
                f.write(message.text.replace("\n", "%n%") + "\n")
            kb = [
                [types.KeyboardButton(text="Конец.")],
            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
            await message.reply(text="Записал...", reply_markup=keyboard)
        else:
            await message.reply(text="Простите, я не понял", reply_markup=types.ReplyKeyboardRemove())
if name == 'main':
executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
