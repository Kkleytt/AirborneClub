from aiogram import Bot, Dispatcher, types  # Основные классы для работы с Telegram Bot API (бот, диспетчер, типы данных).
from aiogram.filters import Command  # Фильтр для обработки команд, отправленных пользователем (например, /start, /help).
from aiogram.types import InlineKeyboardMarkup, CallbackQuery, InlineKeyboardButton  # Создание встроенных клавиатур и обработка нажатий

import commentjson as json  # Библиотека для работы с JSON-данными (чтение, запись, сериализация и десериализация).
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
global cache


async def main():  # Инициализация переменных, запуск бота, чтение конфига
    global loop
    global cache
    cache = {}

    loop = asyncio.get_event_loop()
    data = work_with_cache(
        mode="read"
    )
    if data['result']:
        cache = data['data']
    else:
        cache = {}

    try:
        await utils.log(f"Запуск Telegram-бота с TOKEN='{settings['token']}' на правах - '{settings['database']['settings']['user']}'")
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
                host=settings['database']['settings']['ip'],
                port=settings['database']['settings']['port'],
                user=settings['database']['users'][settings['database']['settings']['user']]['login'],
                password=settings['database']['users'][settings['database']['settings']['user']]['pass'],
                database=settings['database']['settings']['name'],
                connect_timeout=settings['database']['settings']['timeout'],  # Увеличенный timeout подключения,
                read_timeout=settings['database']['settings']['timeout'],  # Увеличенный timeout чтения данных,
                write_timeout=settings['database']['settings']['timeout'],  # Увеличенный timeout записи данных,
                autocommit=True  # Автоматический commit
            )
            self.cursor = self.connection.cursor()

            # Проверяем подключение
            self.cursor.execute("SELECT 1")

            ip = settings["database"]["settings"]["ip"]
            port = settings["database"]["settings"]["port"]
            try:
                text_for_send = f"✅ Успешное подключение к БД по адресу: {ip}:{port}"
                loop.call_soon_threadsafe(asyncio.create_task, utils.error(bot=bot, text=text_for_send, crit=False))
            except Exception as ex:
                print(f"✅ Успешное подключение к БД по адресу: {ip}:{port}\nError - {ex}")

        except pymysql.MySQLError as e:
            ip = settings["database"]["settings"]["ip"]
            port = settings["database"]["settings"]["port"]
            try:
                text_for_send = f"❌ Ошибка подключения к БД по адресу: {ip}:{port}\nError - {e}"
                loop.call_soon_threadsafe(asyncio.create_task, utils.error(bot=bot, text=text_for_send, crit=True))
            except Exception as ex:
                ip = settings["database"]["settings"]["ip"]
                print(f"❌ Ошибка подключения к БД по адресу: {ip}:{port}. Error - {ex}\n ОШИБКА - {e}")

    # Фоновая проверка ping
    @staticmethod
    def start_ping_thread():
        def ping_db():
            while True:
                try:
                    time.sleep(settings["database"]["settings"]["ping"])  # Проверка ping до сервера с БД
                    loop.call_soon_threadsafe(asyncio.create_task, utils.log(f"⚠️ Производится ping БД"))
                    ip = settings["database"]["settings"]["IP"]
                    port = settings["database"]["settings"]["PORT"]
                    with socket.create_connection((ip, port), timeout=5):
                        loop.call_soon_threadsafe(asyncio.create_task, utils.log(f"✅ Сервер MySQL доступен по адресу: {ip}:{port}"))
                except (socket.timeout, ConnectionRefusedError):
                    ip = settings["database"]["settings"]["IP"]
                    port = settings["database"]["settings"]["PORT"]
                    text_for_send = f"❌ Потеря соединения с сервером БД по адресу: {ip}:{port}"
                    loop.call_soon_threadsafe(asyncio.create_task, utils.error(bot=bot, text=text_for_send, crit=True))

        thread = threading.Thread(target=ping_db, daemon=True)
        thread.start()

    # Проверка необходимости переподключения
    def start_update_connection(self):
        def update_connection():
            while True:
                time.sleep(settings["database"]["settings"]["reconnect"])
                loop.call_soon_threadsafe(asyncio.create_task, utils.error(bot=bot, text="♻️ Выполняется переподключение к БД...", crit=False))
                self._connect()
                self.last_reconnect_time = time.time()

        thread = threading.Thread(target=update_connection, daemon=True)
        thread.start()

    # Функция получения всех данных из БД
    def get_all_data(self) -> dict:
        try:
            with self.connection.cursor() as cursor:
                query = "SELECT * FROM messages"
                cursor.execute(query)
                result = cursor.fetchall()
                return {
                    "result": True,
                    "data": result
                }
        except Exception as e:
            print(f'Ошибка получения данных из БД - {e}')
            return {
                "result": False
            }

    # Функция записи кэша в БД
    def save_cache(self, db_cache: dict):
        try:
            with self.connection.cursor() as cursor:
                for item in db_cache:
                    cursor.execute("SELECT chat_id FROM messages WHERE chat_id=%s", (item, ))
                    if cursor.fetchone():
                        cursor.execute(
                            "UPDATE messages SET message_id = %s, user_nic=%s, user_name=%s, last_time=%s, total_query=%s, user_rank=%s WHERE chat_id=%s",
                            (
                                db_cache[item]['last_message_id'],
                                db_cache[item]['user_nic'],
                                db_cache[item]['user_name'],
                                db_cache[item]['last_date'],
                                db_cache[item]['total_query'],
                                db_cache[item]['user_rank'],
                                item
                            )
                        )
                    else:
                        cursor.execute(
                            "INSERT INTO messages (chat_id, message_id, user_nic, user_name, last_time, total_query, user_rank) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                            (
                                item,
                                db_cache[item]['last_message_id'],
                                db_cache[item]['user_nic'],
                                db_cache[item]['user_name'],
                                db_cache[item]['last_date'],
                                db_cache[item]['total_query'],
                                db_cache[item]['user_rank']
                            )
                        )
        except Exception as e:
            print(f"Ошибка записи данных в БД - {e}")


def extract_callback_data(clc: CallbackQuery):
    """Извлекает основные данные из callback-запроса."""
    return {
        "chat_id": clc.message.chat.id,
        "user_nic": clc.from_user.username,
        "user_name": clc.from_user.full_name
    }


# Функция для рекурсивного поиска данных в JSON-структуре
def get_data_from_json(path, data):
    keys = path.split("_")[1:]  # Убираем "airtime"
    for key in keys:
        if "sub" in data and key in data["sub"]:
            data = data["sub"][key]
        else:
            return None  # Если ключ не найден
    return data


# Загрузка структуры JSON
with open('tree.json', 'r', encoding='utf-8') as f:
    TREE_DATA = json.load(f)


# Считывание данных из конфига
with open('config.json', 'r', encoding='utf-8') as file:
    settings = json.load(file)

bot = Bot(token=settings['token'])  # Создание бота с присваиванием токена
dp = Dispatcher()  # Создание тунелированного общения
db = Database()  # Создание сущности БД


# Функция работы с кэшом (чтение - запись)
def work_with_cache(mode):
    """
    Функция для чтения и записи данных в кэш
    :param mode: Параметр режима работы с кэшом
    :return:
    """

    global cache

    match mode:
        case "write":
            try:
                db.save_cache(db_cache=cache)
            except Exception as e:
                print(f"Ошибка записи кэша - {e}")
        case "read":
            try:
                database_data = db.get_all_data()
                if database_data['result']:
                    for item in database_data['data']:
                        cache[int(item[0])] = {
                            'last_message_id': item[1],
                            'user_nic': item[2],
                            'user_name': item[3],
                            'last_date': item[4],
                            'total_query': int(item[5]) if item[5] is not None else 0,
                            'rank': int(item(6)) if item[6] is not None else 0
                        }
                    return {"result": True, "data": cache}
                else:
                    return {"result": False}
            except Exception as e:
                print(f'Ошибка чтения данных из БД - {e}')
                return {"result": False}
        case _:
            print('Некорректно переданный аргумент режима работы mode')
            return {
                "result": False
            }


@dp.message(Command("start"))
async def handle_message(msg: types.Message):
    global cache

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
    cache = await utils.send_message(bot=bot, cache=cache, chat_id=chat_id, message_id=msg_id, user_name=user_name, user_nic=user_nic,
                                     new_text=f"{utils.check_time()}, {user_name}{text.msg_block_hello}",
                                     new_photo=None, new_file=None, keyboard=kb, status=False, del_msg=False)


@dp.message(Command("info"))
async def handle_message(msg: types.Message):
    global cache

    chat_id = msg.chat.id
    msg_id = msg.message_id
    user_nic = msg.from_user.username
    user_name = msg.from_user.full_name

    # Логирование статуса бота
    await utils.log(f"Команда '/info' от (@{user_nic}) [{user_name}]")

    # Создание текста и клавиатуры
    new_message = (
        f"Версия бота\\: {settings['version'].replace(".", "\\.").replace("-", "\\-")}\n"
        f"Дата создания\\: {settings['create'].replace('.', '\\.')}\nСоздатели\\:\n"
        f"  · Руководитель проекта\\: [_Шапарин Юрий Юрьевич_](https://t.me/{settings['creators']['manager']})\n"
        f"  · Автор идеи\\: [_Толстопятова Анна Сергеевна_](https://t.me/{settings['creators']['author']})\n"
        f"  · Редактор\\: [_Толстопятова Анна Сергеевна_](https://t.me/{settings['creators']['writer']})\n"
        f"  · Программист\\: [_Корниецкий Фёдор Алексеевич_](https://t.me/{settings['creators']['programmer']})\n"
        f"  · Тестировщик\\: [_Лихторенко Олеся Сергеевна_](https://t.me/{settings['creators']['tester']})\n"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=text.key_block_info)

    # Изменение прошлого сообщения
    cache = await utils.send_message(bot=bot, cache=cache, chat_id=chat_id, message_id=msg_id, user_name=user_name, user_nic=user_nic,
                                     new_text=new_message, new_photo=None, new_file=None, keyboard=kb, status=True)


@dp.callback_query(lambda c: c.data == "menu")
async def menu_callback(clc: CallbackQuery):
    global cache

    data = extract_callback_data(clc=clc)  # Получение данных о сообщении
    await utils.log(f"Запрос '{clc.data}' от @{data["user_nic"]} [{data["user_name"]}]")

    # Создание клавиатуры с кнопками на основе доступа у пользователя
    if cache[data["chat_id"]]['user_rank'] >= 2:
        result_keyboard = InlineKeyboardMarkup(inline_keyboard=text.key_block_menu_admin)
    else:
        result_keyboard = InlineKeyboardMarkup(inline_keyboard=text.key_block_menu)

    # Отправка сообщения
    cache = await utils.send_message(bot=bot, cache=cache, chat_id=data["chat_id"], message_id=None, user_nic=data["user_nic"],
                                     user_name=data["user_name"], new_text=f"{text.msg_block_menu}",
                                     new_photo=None, new_file=None, keyboard=result_keyboard, status=True)

    # Убираем анимацию загрузки
    await clc.answer()


# Блок "Аэротруба" с дочерними блоками
@dp.callback_query(lambda c: c.data.startswith("airtime"))
async def airtime_callback_handler(clc: types.CallbackQuery):
    global cache

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

    # Отправляем сообщение
    kb = InlineKeyboardMarkup(inline_keyboard=kb)
    cache = await utils.send_message(bot=bot, cache=cache, chat_id=data["chat_id"], message_id=None, user_nic=data["user_nic"],
                                     user_name=data["user_name"], new_text=f"{msg}",
                                     new_photo=send_photo, new_file=send_file, keyboard=kb, status=status)\

    # Убираем анимацию загрузки
    await clc.answer()


# Блок "Прыжки" с дочерними блоками
@dp.callback_query(lambda c: c.data.startswith("jumping"))
async def airtime_callback_handler(clc: types.CallbackQuery):
    global cache

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
    cache = await utils.send_message(bot=bot, cache=cache, chat_id=data["chat_id"], message_id=None, user_nic=data["user_nic"],
                                     user_name=data["user_name"], new_text=f"{msg}",
                                     new_photo=send_photo, new_file=send_file, keyboard=kb, status=status)

    # Убираем анимацию загрузки
    await clc.answer()


# Блок "Соревнования" с дочерними блоками
@dp.callback_query(lambda c: c.data.startswith("competitions"))
async def airtime_callback_handler(clc: types.CallbackQuery):
    global cache

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
    cache = await utils.send_message(bot=bot, cache=cache, chat_id=data["chat_id"], message_id=None, user_nic=data["user_nic"],
                                     user_name=data["user_name"], new_text=f"{msg}",
                                     new_photo=send_photo, new_file=send_file, keyboard=kb, status=status)

    # Убираем анимацию загрузки
    await clc.answer()


# Блок "Дополнительно" с дочерними блоками
@dp.callback_query(lambda c: c.data.startswith("additionally"))
async def airtime_callback_handler(clc: types.CallbackQuery):
    global cache

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
    cache = await utils.send_message(bot=bot, cache=cache, chat_id=data["chat_id"], message_id=None, user_nic=data["user_nic"],
                                     user_name=data["user_name"], new_text=f"{msg}",
                                     new_photo=send_photo, new_file=send_file, keyboard=kb, status=status)

    # Убираем анимацию загрузки
    await clc.answer()


# Блок "О нас" с дочерними блоками
@dp.callback_query(lambda c: c.data.startswith("about"))
async def airtime_callback_handler(clc: types.CallbackQuery):
    global cache

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
    cache = await utils.send_message(bot=bot, cache=cache, chat_id=data["chat_id"], message_id=None, user_nic=data["user_nic"],
                                     user_name=data["user_name"], new_text=f"{msg}",
                                     new_photo=send_photo, new_file=send_file, keyboard=kb, status=status)

    # Убираем анимацию загрузки
    await clc.answer()


# Блок с администрированием бота и его пользователей4
@dp.callback_query(lambda c: c.data.startswith("admin"))
async def block_admin_panel(clc: types.CallbackQuery):
    pass


if __name__ == "__main__":
    try:
        asyncio.run(main())  # Асинхронный запуск выполнения кода
    finally:
        work_with_cache(mode="write")
        exit(0)
