from aiogram import Bot, Dispatcher, types  # Основные классы для работы с Telegram Bot API (бот, диспетчер, типы данных).
from aiogram.filters import Command  # Фильтр для обработки команд, отправленных пользователем (например, /start, /help).
from aiogram.types import InlineKeyboardMarkup, CallbackQuery  # Создание встроенных клавиатур и обработка нажатий

import json  # Библиотека для работы с JSON-данными (чтение, запись, сериализация и десериализация).
import asyncio  # Библиотека для работы с асинхронными функциями и управления асинхронными задачами.
import pymysql  # Библиотека для подключения и работы с базами данных MySQL через Python.
import os  # Библиотека для работы с файловой системой и взаимодействия с операционной средой.
import time  # Библиотека для работы со временем (измерение времени, задержки, обработка временных меток).
import threading  # Библиотека для работы с многопоточностью и параллельным выполнением задач.
import socket  # Библиотека для отправки TCP/UDP запросов.

import utils  # Библиотека с доп функционалом
import text  # Библиотека с текстами и клавиатурами для вывода сообщений

images_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')
files_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files')

global loop


async def main():  # Инициализация переменных, запуск бота, чтение конфига
    global loop

    loop = asyncio.get_event_loop()

    try:
        await utils.log(f"Запуск Telegram-бота с TOKEN='{CONFIG['TOKEN']}' на правах - '{CONFIG['DATABASE']['SETTINGS']['STANDARD_USER']}'")
        await dp.start_polling(bot)
    finally:
        await utils.error(bot=bot, text=f"❌ Бот прекратил свою работу", crit=True)
        exit(0)


class Database:
    def __init__(self):
        self._connect()
        self.start_update_connection()  # Запуск фоновой проверки переподключения
        self.start_ping_thread()  # Запуск фоновой проверки ping

    # Функция подключения к БД
    def _connect(self):
        try:
            self.connection = pymysql.connect(
                host=CONFIG["DATABASE"]["SETTINGS"]["IP"],
                port=CONFIG["DATABASE"]["SETTINGS"]["PORT"],
                user=CONFIG["DATABASE"]["USERS"][CONFIG["DATABASE"]["SETTINGS"]["STANDARD_USER"]]["LOGIN"],
                password=CONFIG["DATABASE"]["USERS"][CONFIG["DATABASE"]["SETTINGS"]["STANDARD_USER"]]["PASSWORD"],
                database=CONFIG["DATABASE"]["SETTINGS"]["NAME"],
                connect_timeout=CONFIG["DATABASE"]["SETTINGS"]["TIMEOUT"],  # Увеличенный timeout подключения,
                read_timeout=CONFIG["DATABASE"]["SETTINGS"]["TIMEOUT"],  # Увеличенный timeout чтения данных,
                write_timeout=CONFIG["DATABASE"]["SETTINGS"]["TIMEOUT"],  # Увеличенный timeout записи данных,
                autocommit=True  # Автоматический commit
            )
            self.cursor = self.connection.cursor()

            # Проверяем подключение
            self.cursor.execute("SELECT 1")

            ip = CONFIG["DATABASE"]["SETTINGS"]["IP"]
            port = CONFIG["DATABASE"]["SETTINGS"]["PORT"]
            try:
                text_for_send = f"✅ Успешное подключение к БД по адресу: {ip}:{port}"
                loop.call_soon_threadsafe(asyncio.create_task, utils.error(bot=bot, text=text_for_send, crit=False))
            except Exception as ex:
                print(f"✅ Успешное подключение к БД по адресу: {ip}:{port}\nError - {ex}")

        except pymysql.MySQLError as e:
            ip = CONFIG["DATABASE"]["SETTINGS"]["IP"]
            port = CONFIG["DATABASE"]["SETTINGS"]["PORT"]
            try:
                text_for_send = f"❌ Ошибка подключения к БД по адресу: {ip}:{port}\nError - {e}"
                loop.call_soon_threadsafe(asyncio.create_task, utils.error(bot=bot, text=text_for_send, crit=True))
            except Exception as ex:
                ip = CONFIG["DATABASE"]["SETTINGS"]["IP"]
                print(f"❌ Ошибка подключения к БД по адресу: {ip}:{port}. Error - {ex}\n ОШИБКА - {e}")

    # Фоновая проверка ping
    @staticmethod
    def start_ping_thread():
        def ping_db():
            while True:
                try:
                    time.sleep(CONFIG["DATABASE"]["SETTINGS"]["CHECK_PING"])  # Проверка ping до сервера с БД
                    loop.call_soon_threadsafe(asyncio.create_task, utils.log(f"⚠️ Производится ping БД"))
                    ip = CONFIG["DATABASE"]["SETTINGS"]["IP"]
                    port = CONFIG["DATABASE"]["SETTINGS"]["PORT"]
                    with socket.create_connection((ip, port), timeout=5):
                        loop.call_soon_threadsafe(asyncio.create_task, utils.log(f"✅ Сервер MySQL доступен по адресу: {ip}:{port}"))
                except (socket.timeout, ConnectionRefusedError):
                    ip = CONFIG["DATABASE"]["SETTINGS"]["IP"]
                    port = CONFIG["DATABASE"]["SETTINGS"]["PORT"]
                    text_for_send = f"❌ Потеря соединения с сервером БД по адресу: {ip}:{port}"
                    loop.call_soon_threadsafe(asyncio.create_task, utils.error(bot=bot, text=text_for_send, crit=True))

        thread = threading.Thread(target=ping_db, daemon=True)
        thread.start()

    # Проверка необходимости переподключения
    def start_update_connection(self):
        def update_connection():
            while True:
                time.sleep(CONFIG["DATABASE"]["SETTINGS"]["RE_CONNECT"])
                loop.call_soon_threadsafe(asyncio.create_task, utils.error(bot=bot, text="♻️ Выполняется переподключение к БД...", crit=False))
                self._connect()
                self.last_reconnect_time = time.time()

        thread = threading.Thread(target=update_connection, daemon=True)
        thread.start()

    # Получение message_id
    def get_message(self, chat_id):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT message_id FROM messages WHERE chat_id = %s", (chat_id,))
            result = cursor.fetchone()
            if result:
                return None if result[0] == "None" else result[0]
            else:
                return False

    # Сохранение данных в БД
    def save_full_message(self, chat_id, message_id, user_nic, user_name, last_time):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM messages WHERE chat_id = %s", (chat_id,))
            if cursor.fetchone():
                cursor.execute(
                    "UPDATE messages SET message_id = %s, last_time = %s WHERE chat_id = %s",
                    (message_id, last_time, chat_id)
                )
            else:
                cursor.execute(
                    "INSERT INTO messages (chat_id, message_id, user_nic, user_name, last_time) VALUES (%s, %s, %s, %s, %s)",
                    (chat_id, message_id, user_nic, user_name, last_time)
                )

    # Обновление времени последнего захода
    def update_time(self, chat_id, last_time):
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE messages SET last_time = %s WHERE chat_id = %s", (last_time, chat_id))


def extract_callback_data(clc: CallbackQuery):
    """Извлекает основные данные из callback-запроса."""
    return {
        "chat_id": clc.message.chat.id,
        "user_nic": clc.from_user.username,
        "user_name": clc.from_user.full_name
    }


def get_data_from_json(path, data):
    keys = path.split("_")[1:]  # Убираем "airtime"
    for key in keys:
        if "sub" in data and key in data["sub"]:
            data = data["sub"][key]
        else:
            return None  # Если ключ не найден
    return data


# Загрузка структуры JSON
with open("tree.json", "r", encoding="utf-8") as f:
    TREE_DATA = json.load(f)


# Считывание данных из конфига
with open("config.json", "r") as file:
    CONFIG = json.load(file)

bot = Bot(token=CONFIG['TOKEN'])  # Создание бота с присваиванием токена
dp = Dispatcher()  # Создание тунелированного общения
db = Database()  # Создание сущности БД


@dp.message(Command("start"))
async def start_handle_message(msg: types.Message):
    chat_id = msg.chat.id
    msg_id = msg.message_id
    user_nic = msg.from_user.username
    user_name = msg.from_user.full_name

    # Логирование статуса бота
    await utils.log(f"Команда '/start' от (@{user_nic}) [{user_name}]")

    # Отправка нулевого сообщения, для обхода пустой истории Telegram
    await bot.send_message(chat_id, text=text.msg_block_zero, parse_mode="MarkdownV2")

    # Создание клавиатуры и отправка нового сообщения
    kb = InlineKeyboardMarkup(inline_keyboard=text.key_block_hello)
    await utils.send_message(bot=bot, db=db, chat_id=chat_id, message_id=msg_id, user_name=user_name, user_nic=user_nic,
                             new_text=f"{utils.check_time()}, {user_name}{text.msg_block_hello}",
                             new_photo=None, new_file=None, keyboard=kb, status=False, del_msg=False)


@dp.message(Command("info"))
async def info_handle_message(msg: types.Message):
    chat_id = msg.chat.id
    msg_id = msg.message_id
    user_nic = msg.from_user.username
    user_name = msg.from_user.full_name

    # Логирование статуса бота
    await utils.log(f"Команда '/info' от (@{user_nic}) [{user_name}]")

    # Создание текста и клавиатуры
    new_message = (
        f"Версия бота\\: {CONFIG['VERSION_BOT'].replace(".", "\\.").replace("-", "\\-")}\n"
        f"Дата создания\\: {CONFIG['DATA_CREATE'].replace('.', '\\.')}\nСоздатели\\:\n"
        f"  · Руководитель проекта\\: [_Шапарин Юрий Юрьевич_](https://t.me/{CONFIG['CREATORS']['PROJECT_MANAGER']})\n"
        f"  · Автор идеи\\: [_Толстопятова Анна Сергеевна_](https://t.me/{CONFIG['CREATORS']['IDEA_AUTHOR']})\n"
        f"  · Редактор\\: [_Толстопятова Анна Сергеевна_](https://t.me/{CONFIG['CREATORS']['WRITER']})\n"
        f"  · Программист\\: [_Корниецкий Фёдор Алексеевич_](https://t.me/{CONFIG['CREATORS']['PROGRAMMER']})\n"
        f"  · Тестировщик\\: [_Лихторенко Олеся Сергеевна_](https://t.me/{CONFIG['CREATORS']['TESTER']})\n"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=text.key_block_info)

    # Изменение прошлого сообщения
    await utils.send_message(bot=bot, db=db, chat_id=chat_id, message_id=msg_id, user_name=user_name, user_nic=user_nic,
                             new_text=new_message, new_photo=None, new_file=None, keyboard=kb, status=True)


@dp.callback_query(lambda c: c.data == "menu")
async def menu_callback_handler(clc: CallbackQuery):
    data = extract_callback_data(clc=clc)  # Получение данных о сообщении
    await utils.log(f"Запрос '{clc.data}' от @{data["user_nic"]} [{data["user_name"]}]")

    # Создание клавиатуры с кнопками и отправка сообщения
    kb = InlineKeyboardMarkup(inline_keyboard=text.key_block_menu)
    await utils.send_message(bot=bot, db=db, chat_id=data["chat_id"], message_id=None, user_nic=data["user_nic"],
                             user_name=data["user_name"], new_text=f"{text.msg_block_menu}",
                             new_photo=None, new_file=None, keyboard=kb, status=True)
    await clc.answer()  # Убираем анимацию загрузки


# Блок "Аэротруба" с дочерними блоками
@dp.callback_query(lambda c: c.data.startswith("airtime"))
async def airtime_callback_handler(clc: types.CallbackQuery):
    data = extract_callback_data(clc=clc)  # Получение данных о сообщении
    await utils.log(f"Запрос '{clc.data}' от @{data["user_nic"]} [{data["user_name"]}]")

    # Извлекаем нужный блок данных
    query_data = get_data_from_json(clc.data, TREE_DATA.get("airtime", {}))

    if not query_data:
        await clc.answer("Раздел недоступен, дождитесь обновления", show_alert=True)
        return

    # Получаем текст, клавиатуру, фото и файл из text.py
    msg = eval("text." + query_data["text"]) if query_data["text"] != "None" else None
    kb = eval("text." + query_data["keyboard"]) if query_data["keyboard"] != "None" else None
    send_photo = eval("text." + query_data["photo"]) if query_data["photo"] != "None" else None
    send_file = eval("text." + query_data["file"]) if query_data["file"] != "None" else None
    status = eval(query_data["status"]) if query_data["status"] != "None" else False

    kb = InlineKeyboardMarkup(inline_keyboard=kb)
    await utils.send_message(bot=bot, db=db, chat_id=data["chat_id"], message_id=None, user_nic=data["user_nic"],
                             user_name=data["user_name"], new_text=f"{msg}",
                             new_photo=send_photo, new_file=send_file, keyboard=kb, status=status)


# Блок "Прыжки" с дочерними блоками
@dp.callback_query(lambda c: c.data.startswith("jumping"))
async def jumping_callback_handler(clc: types.CallbackQuery):
    data = extract_callback_data(clc=clc)  # Получение данных о сообщении
    await utils.log(f"Запрос '{clc.data}' от @{data["user_nic"]} [{data["user_name"]}]")

    # Извлекаем нужный блок данных
    query_data = get_data_from_json(clc.data, TREE_DATA.get("jumping", {}))

    if not query_data:
        await clc.answer("Раздел недоступен, дождитесь обновления", show_alert=True)
        return

    # Получаем текст, клавиатуру, фото и файл из text.py
    msg = eval("text." + query_data["text"]) if query_data["text"] != "None" else None
    kb = eval("text." + query_data["keyboard"]) if query_data["keyboard"] != "None" else None
    send_photo = eval("text." + query_data["photo"]) if query_data["photo"] != "None" else None
    send_file = eval("text." + query_data["file"]) if query_data["file"] != "None" else None
    status = eval(query_data["status"]) if query_data["status"] != "None" else False

    kb = InlineKeyboardMarkup(inline_keyboard=kb)
    await utils.send_message(bot=bot, db=db, chat_id=data["chat_id"], message_id=None, user_nic=data["user_nic"],
                             user_name=data["user_name"], new_text=f"{msg}",
                             new_photo=send_photo, new_file=send_file, keyboard=kb, status=status)


# Блок "Соревнования" с дочерними блоками
@dp.callback_query(lambda c: c.data.startswith("competitions"))
async def competitions_callback_handler(clc: types.CallbackQuery):
    data = extract_callback_data(clc=clc)  # Получение данных о сообщении
    await utils.log(f"Запрос '{clc.data}' от @{data["user_nic"]} [{data["user_name"]}]")

    # Извлекаем нужный блок данных
    query_data = get_data_from_json(clc.data, TREE_DATA.get("competitions", {}))

    if not query_data:
        await clc.answer("Раздел недоступен, дождитесь обновления", show_alert=True)
        return

    # Получаем текст, клавиатуру, фото и файл из text.py
    msg = eval("text." + query_data["text"]) if query_data["text"] != "None" else None
    kb = eval("text." + query_data["keyboard"]) if query_data["keyboard"] != "None" else None
    send_photo = eval("text." + query_data["photo"]) if query_data["photo"] != "None" else None
    send_file = eval("text." + query_data["file"]) if query_data["file"] != "None" else None
    status = eval(query_data["status"]) if query_data["status"] != "None" else False

    kb = InlineKeyboardMarkup(inline_keyboard=kb)
    await utils.send_message(bot=bot, db=db, chat_id=data["chat_id"], message_id=None, user_nic=data["user_nic"],
                             user_name=data["user_name"], new_text=f"{msg}",
                             new_photo=send_photo, new_file=send_file, keyboard=kb, status=status)


# Блок "Дополнительно" с дочерними блоками
@dp.callback_query(lambda c: c.data.startswith("additionally"))
async def additionally_callback_handler(clc: types.CallbackQuery):
    data = extract_callback_data(clc=clc)  # Получение данных о сообщении
    await utils.log(f"Запрос '{clc.data}' от @{data["user_nic"]} [{data["user_name"]}]")

    # Извлекаем нужный блок данных
    query_data = get_data_from_json(clc.data, TREE_DATA.get("additionally", {}))

    if not query_data:
        await clc.answer("Раздел недоступен, дождитесь обновления", show_alert=True)
        return

    # Получаем текст, клавиатуру, фото и файл из text.py
    msg = eval("text." + query_data["text"]) if query_data["text"] != "None" else None
    kb = eval("text." + query_data["keyboard"]) if query_data["keyboard"] != "None" else None
    send_photo = eval("text." + query_data["photo"]) if query_data["photo"] != "None" else None
    send_file = eval("text." + query_data["file"]) if query_data["file"] != "None" else None
    status = eval(query_data["status"]) if query_data["status"] != "None" else False

    kb = InlineKeyboardMarkup(inline_keyboard=kb)
    await utils.send_message(bot=bot, db=db, chat_id=data["chat_id"], message_id=None, user_nic=data["user_nic"],
                             user_name=data["user_name"], new_text=f"{msg}",
                             new_photo=send_photo, new_file=send_file, keyboard=kb, status=status)


# Блок "О нас" с дочерними блоками
@dp.callback_query(lambda c: c.data.startswith("about"))
async def about_callback_handler(clc: types.CallbackQuery):
    data = extract_callback_data(clc=clc)  # Получение данных о сообщении
    await utils.log(f"Запрос '{clc.data}' от @{data["user_nic"]} [{data["user_name"]}]")

    # Извлекаем нужный блок данных
    query_data = get_data_from_json(clc.data, TREE_DATA.get("about", {}))

    if not query_data:
        await clc.answer("Раздел недоступен, дождитесь обновления", show_alert=True)
        return

    # Получаем текст, клавиатуру, фото и файл из text.py
    msg = eval("text." + query_data["text"]) if query_data["text"] != "None" else None
    kb = eval("text." + query_data["keyboard"]) if query_data["keyboard"] != "None" else None
    send_photo = eval("text." + query_data["photo"]) if query_data["photo"] != "None" else None
    send_file = eval("text." + query_data["file"]) if query_data["file"] != "None" else None
    status = eval(query_data["status"]) if query_data["status"] != "None" else False

    kb = InlineKeyboardMarkup(inline_keyboard=kb)
    await utils.send_message(bot=bot, db=db, chat_id=data["chat_id"], message_id=None, user_nic=data["user_nic"],
                             user_name=data["user_name"], new_text=f"{msg}",
                             new_photo=send_photo, new_file=send_file, keyboard=kb, status=status)


if __name__ == "__main__":
    try:
        asyncio.run(main())  # Асинхронный запуск выполнения кода
    finally:
        exit(0)
