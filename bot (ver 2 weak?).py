import os # подключение модуля для работы с операционной системой
from aiogram import Bot, Dispatcher, executor, types # импорт классов из библиотеки aiogram
import time # подключение модуля для работы со временем 

API_TOKEN = '6245533640:AAFa5p1awQe4H0tQhoi7TEQxHPgX993P69E' # токен для доступа к Telegram API

botQuest = Bot(token=API_TOKEN) # создание экземпляра класса Bot из aiogram
dp = Dispatcher(botQuest) # создание диспетчера для бота
story_wait = False # переменная для отслеживания состояния бота
now_w = False
story_name = '' #  переменная для хранения имени текущей истории


@dp.message_handler(commands=['start'])  # Явно указываем в декораторе, на какую команду реагируем.
async def send_welcome(message: types.Message): # функция-обработчик для команды /start
    kb = [
        [types.KeyboardButton(text="Я хочу создать свой собственный квест!", callback_data='ready_tw')], #Создаём на выбор две кнопки клавиатуры,
        [types.KeyboardButton(text="Я хочу прочесть истории других людей!", callback_data='ready_tr')]   #чтобы бот определил, что хочет пользователь
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True) #создание клавиатуры
    welcome_message = f"Приветствую тебя, поэт-путник, в мире стихов и рифм! \n Я твой верный помощник, бот, " \
                      f"но душа у меня жива. \n Записывать и читать стихи - вот мое призвание, \n С радостью я помогу "\
                      f"воплотить в них твое вдохновение. "
    await message.reply(welcome_message, reply_markup=keyboard)  # Так как код работает асинхронно, то обязательно
    # пишем await.


@dp.message_handler()  # Создаём новое событие, которое запускается в ответ на любой текст, введённый пользователем.
async def communicate(message: types.Message): #функция-обработчик для всех текстовых сообщений пользователей
    callback_data = message.text
    # (callback_data)

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
        await message.answer("Я начинаю рассказ...")
        time.sleep(2) # задержка программы на 2 секунды
        f = open(f'data/{callback_data}.txt', 'r', encoding='UTF-8') #открытие текстового файла для чтения
        lines = f.read().split('\n') # чтение строк из файла и разделение их на список
        for line in lines:
            # print(line)
            await message.answer(line.replace("%n%", "\n")) # отправка пользователям строки с заменой "%n%" на переносы строк
            delay = len(line) * 0.08
            time.sleep(delay)
    else:
        match callback_data: # оператор сопоставления
            case "Начнём запись":
                await message.reply(text="Хорошо, начнём! Сначала название, потом всё остальное.",
                                    reply_markup=types.ReplyKeyboardRemove())

            case "Я хочу создать свой собственный квест!":
                await message.reply(text="Отлично. Подтверди свой выбор!", reply_markup=types.ReplyKeyboardRemove())
                kb = [
                    [types.KeyboardButton(text="Начнём запись", callback_data='writing')],
                    [types.KeyboardButton(text="Я передумал - не нужно начинать запись", callback_data='ready_tr')]
                ]
                keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
                time.sleep(0.02)
                await message.reply("...", reply_markup=keyboard)

            case "Я хочу прочесть истории других людей!" | "Список":
                await message.reply("Вот список")
                stores = os.listdir("data")
                for story in stores:
                    await message.answer(story.replace("%n%", "\n")[:-4]) # отправка пользователю названия истории с удалением ".txt" в конце
                    delay = len(story) * 0.08
                    time.sleep(delay)
            case "Я передумал - не нужно начинать запись":
                await message.reply("Хорошо. Я не настаиваю", reply_markup=types.ReplyKeyboardRemove())
            case "Конец.":
                await message.reply("Запись завершена", reply_markup=types.ReplyKeyboardRemove())
            case _:
                if now_w:
                    f = open(f'data/{story_name}.txt', 'a', encoding='UTF-8') # открытие текстового файла для записи, с дозаписью в конец
                    f.write(message.text.replace("\n", "%n%") + "\n")
                    kb = [
                        [types.KeyboardButton(text="Конец.")],
                    ]
                    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
                    await message.reply(text="Записал...", reply_markup=keyboard) # отправка сообщения пользователю и клавиатуры
                else:
                    await message.reply(text="Простите, я не понял", reply_markup=types.ReplyKeyboardRemove())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
