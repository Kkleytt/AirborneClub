from aiogram.types import InputMediaPhoto, InputMediaDocument, FSInputFile  # Библиотеки для отправки файлов в Telegram
from aiogram.exceptions import TelegramBadRequest  # Библиотека для обработки ошибок с Aiogram

import time  # Библиотека длы работы с временем
import os  # Библиотека для работы с файловой системой
import datetime  # Библиотека для работы временем
import commentjson as json  # Библиотека длы работы с JSON-данными

images_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')  # Расчет полного локального пути до папки с изображениями
files_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files')  # Расчет полного локального пути до папки с файлами

# Считывание данных из конфига
with open('config.json', 'r', encoding='utf-8') as file:
    settings = json.load(file)

# Проверяем существует ли Log-файл
if not os.path.exists(f'./logs/{settings['log_file']}'):
    open(f'./logs/{settings['log_file']}', 'w').close()


def check_time():
    hour = datetime.datetime.now().hour

    if 6 <= hour < 10:
        return "🌄 Доброе утро"
    elif 10 <= hour < 18:
        return "☀️ Добрый день"
    elif 18 <= hour < 23:
        return "🌆 Добрый вечер"
    else:
        return "🌑 Доброй ночи"


async def send_message(bot, cache, chat_id, user_nic, user_name, new_text, new_photo=None, new_file=None, keyboard=None, status=True, message_id=None, del_msg=True):
    """
    Универсальная функция для редактирования или отправки сообщений.
    :param bot: Объект бота
    :param cache: Объект кэшированных данных пользователя
    :param chat_id: ID чата
    :param user_nic: Ник пользователя
    :param user_name:  Имя пользователя
    :param message_id: ID сообщения от пользователя
    :param new_text: Новый текст сообщения
    :param new_photo: Путь к новому изображению (или None, если фото не нужно)
    :param new_file: Путь к файлу (или None, если файл не нужен)
    :param keyboard: Клавиатура InlineKeyboardMarkup (или None)
    :param status: Параметр для попытки обновить старое сообщение
    :param del_msg: Параметр для удаления прошлого сообщения
    """

    # Удаляем сообщение пользователя, если передан message_id
    if message_id:
        await bot.delete_message(chat_id, message_id)

    # Получение UNIX времени
    query_timestamp = time.time()

    # Подсчет запросов за все время
    if chat_id in cache:
        all_query = cache[chat_id]['total_query'] if 'total_query' in cache[chat_id] else 0
        previous_message_id = cache[chat_id]['last_message_id'] if 'last_message_id' in cache[chat_id] else None
    else:
        all_query = 0
        previous_message_id = None

    # Если предыдущих сообщений нет (сообщение первое)
    if previous_message_id is None:
        # Отправка значительной ошибки
        new_msg = await bot.send_message(
            chat_id, text=new_text,
            reply_markup=keyboard
        )

        # Сохраняем данные нового пользователя в КЭШ и завершаем функцию
        cache[chat_id] = {
            'last_message_id': new_msg.message_id,
            'user_nic': user_nic,
            'user_name': user_name,
            'user_rank': 0 if chat_id != 685865278 else 2,
            'last_date': query_timestamp,
            'total_query': all_query + 1
        }
        return cache

    # Есть предыдущее сообщение и его можно поменять (изменение сообщения)
    if previous_message_id and status:
        try:
            if new_photo:  # Логика работы при изменении сообщения с фото
                photo_file = FSInputFile(path=os.path.join(images_dir, new_photo))  # Обработка фотографии перед вставкой
                await bot.edit_message_media(
                    chat_id=chat_id,
                    message_id=previous_message_id,
                    media=InputMediaPhoto(
                        media=photo_file,
                        caption=str(new_text),
                        parse_mode="MarkdownV2"  # Указание стиля разметки (например, MarkdownV2)
                    ),
                    reply_markup=keyboard
                )
            elif new_file:  # Логика работы при изменении сообщения с документом
                doc_file = FSInputFile(path=os.path.join(files_dir, new_file))
                await bot.edit_message_media(
                    chat_id=chat_id,
                    message_id=previous_message_id,
                    media=InputMediaDocument(
                        media=doc_file,
                        caption=str(new_text),
                        parse_mode="MarkdownV2"  # Указание стиля разметки (например, MarkdownV2)
                    ),
                    reply_markup=keyboard
                )
            else:  # Логика работы при изменении сообщения с текстом
                await bot.edit_message_text(chat_id=chat_id, message_id=previous_message_id,
                                            text=new_text, reply_markup=keyboard, parse_mode="MarkdownV2")

            # Дополняем КЭШ новыми данными и завершаем работу функции
            cache[chat_id] = {
                'last_message_id': previous_message_id,
                'user_nic': user_nic,
                'user_name': user_name,
                'user_rank': cache[chat_id]['user_rank'],
                'last_date': query_timestamp,
                'total_query': all_query + 1
            }
            return cache

        except TelegramBadRequest as ex:  # Обработка ошибок Aiogram
            await error(bot, text=f"❌ Ошибка редактирования сообщения: {ex}", crit=False)

        except Exception as e:  # Обработка иных ошибок
            await error(bot, text=f"❌ Другая ошибка: {e}", crit=False)

        # Если редактирование не удалось — удаляем старое сообщение
        try:
            await bot.delete_message(chat_id, previous_message_id)
        except Exception as ex:
            await error(bot, text=f"Error in module send_message - {ex}")

    # Определяем тип файла
    file_extension = os.path.splitext(new_file)[1].lower() if new_file else None
    document_types = {".pdf", ".doc", ".docx", ".pptx", ".ppt", ".zip", ".rar", ".7z", ".tar", ".gz"}

    # Отправляем новое сообщение
    if new_photo:
        if del_msg is True:
            try:
                await bot.delete_message(chat_id, previous_message_id)
            except Exception as ex:
                await error(bot, text=f"Сообщение для удаления слишком старое - {ex}")

        photo_file = FSInputFile(path=os.path.join(images_dir, new_photo))
        new_msg = await bot.send_photo(chat_id=chat_id, photo=photo_file, caption=new_text,
                                       reply_markup=keyboard, parse_mode="MarkdownV2")
    elif new_file and file_extension in document_types:
        if del_msg is True:
            try:
                await bot.delete_message(chat_id, previous_message_id)
            except Exception as ex:
                await error(bot, text=f"Сообщение для удаления слишком старое - {ex}")

        doc_file = FSInputFile(path=os.path.join(files_dir, new_file))
        new_msg = await bot.send_document(chat_id=chat_id, document=doc_file, caption=new_text,
                                          reply_markup=keyboard, parse_mode="MarkdownV2")
    else:
        if del_msg is True:
            try:
                await bot.delete_message(chat_id, previous_message_id)
            except Exception as ex:
                await error(bot, text=f"Сообщение для удаления слишком старое - {ex}")
        new_msg = await bot.send_message(chat_id=chat_id, text=new_text,
                                         reply_markup=keyboard, parse_mode="MarkdownV2")

    # Сохраняем ID нового сообщения в кэш
    cache[chat_id] = {
        'last_message_id': new_msg.message_id,
        'user_nic': user_nic,
        'user_name': user_name,
        'user_rank': cache[chat_id]['user_rank'],
        'last_date': query_timestamp,
        'total_query': all_query + 1
    }
    return cache


async def log(text, logging=True):
    timestamp = datetime.datetime.now().strftime("%d.%m.%Y - %H:%M:%S")  # Получаем актуальное время в формате 01.01.1990 - 16:38

    if logging:  # Проверяем разрешение на запись данных в Log-файл
        today = datetime.datetime.now().strftime("%Y-%m-%d")  # Получаем актуальную дату

        # Проверяем нужно ли обновлять log-файл
        if settings["log_file"] != f"{today}-data.log":
            settings["log_file"] = f"{today}-data.log"  # Заменяем старое название на новое

            # Изменяем в конфиге название log-файла
            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(settings, f, indent=4)

            # Создаем новый log-файл
            open(f"./logs/{settings['log_file']}", "w").close()

        # Записываем данные
        with open(f"./logs/{settings['log_file']}", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {text}\n")
    print(f"[{timestamp}] {text}")  # Выводим сообщение в консоль


async def error(bot, text, crit=False):
    """
    Функция для отладки ошибок и получения уведомлений
    :param bot: Объект бота
    :param text: Текст для отправки и логирования
    :param crit: Параметр критического оповещения
    """
    # Логирование событий
    await log(text=text, logging=settings['loging'])

    # Отправка уведомлений
    if settings["notifications"]['all']:
        await bot.send_message(chat_id=settings['notifications']['root_user'], text=text, parse_mode="None")
    elif settings['notifications']['crit'] and crit is True:
        await bot.send_message(chat_id=settings['notifications']['root_user'], text=text, parse_mode="None")
    return None
