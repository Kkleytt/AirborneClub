Разбор модулей:
	- bot.py (Основной файл бота, где происходит обмен сообщениями и работа с БД)
	- utils.py (Файл в котором расположены доп функции для работы бота)
	- text.py (Файл в котором хранятся все текстовые сообщения, клавиатуры, ссылки на изображения и файлы)
	- config.json (Основные настройки бота, которые не могут изменяться)
	- tree.json (Дерево интерфейса бота)
	- data.log (Файл событий, в который записываются все события в боте)
	- images (Директория в которой хранятся изображения)
	- files (Директория в которой хранятся документы, видео, файлы)
	
Разбор функций:
	bot.py
		main() - Функция асинхронного запуска бота и всех дочерних процессов
		Database() - Объект базы данных
			__init__() - Инициализация БД и запуск дочерних процессов
			_connect() - Функция для подключения к БД и логирования статусов
			start_ping_thread() - Функция таймера, для определния ping каждые [15 минут]
			start_update_connection() - Функция таймера, для переподключения к БД каждые [2 часа]
			get_message() - Функция получения message_id послнего сообщения от бота конкретному пользователю
			save_message() - Функция сохранения данных о пользователе (chat_id, message_id, user_nic, user_name, last_time)
			update_time() - Функция обновления данных о последнем заходе пользователя
		exctract_callback_data(clc) - Функция получения данных из callback вызова (chat_id, user_nic, user_name)
		get_data_from_json() - Функция поиска параметров сообщения в структуре json
		start_handle_message() - Функция обрабатывающая команду "/start"
		info_handle_message() - Функция обрабатывающая команду "/info"
		menu_callback_handler() - Функция обрабатывающая callback-вызов "Главное меню"
		airtime_callback_handler() - Функция обрабатывающая callback-вызовы в меню "Аэротруба"
		jumping_callback_handler() - Функция обрабатывающая callback-вызовы в меню "Прыжки"
		competitions_callback_handler() - Функция обрабатывающая callback-вызовы в меню "Соревнования"
		additionally_callback_handler() - Функция обрабатывающая callback-вызовы в меню "Дополнительно"
		about_callback_handler() - Функция обрабатывающая callback-вызовы в меню "О нас"
	utils.py
		check_time() - Функция генерации приветствия относительно времени суток
		send_message() - Функция отправки и изменения сообщений в боте
		log() - Функция записи событий в LOG и вывода их в консоль
		error() - Функция для логирования ошибок и отправки оповещений Администратору
	text.py
		msg_block_{} - Сообщение, которое будет отправляено с определенном блоке, оформлено по стандартам "MarkdownV2"
		key_block_{} - Прикрепленная клавиатура, которая будет отправлена вместе с сообщением
		img_block_{} - Изображение, которое будет отправленно вместе с сообщением
		file_block_{} - Файл, который будет отправлен вместе с сообщением
		
		
Параметры send_message():
	bot - Объект бота для взаимодействия с TelegramAPI
	db - Объект базы данных для взаимодействия с БД
	chat_id - Идентификатор чата для работы с ним
	user_nic - Ник-нейм пользователя
	user_name - Полное имя пользователя
	new_text - Новый текст для отправки или замены старого сообщения
	new_photo - Название фотографии для отправки или замены старой
	new_file - Название файла для отправки или замены старого
	keyboard - Клавиатура для прикрепления к сообщению
	status - Разрешение на изменени сообщения (True-изменяем старое сообщение, False-сразу отправляем новое)
	message_id - Сообщение от пользователя для его удаления (None-если пользователь ничего не отправлял)
	del_msg - Параметр для удаления прошлого сообщения
	
	ПРИМЕРЫ:
		- await utils.send_message(bot=bot, db=db, chat_id=data["chat_id"], message_id=None, user_nic=data["user_nic"],
            user_name=data["user_name"], new_text=f"{text.msg_block_menu}",
            new_photo=None, new_file=None, keyboard=kb, status=True) - Вызов сообщения с попыткой изменить прошлое сообщение, без фото и файлов, а также без удаления сообщения от пользователя
		- await utils.send_message(bot=bot, db=db, chat_id=data["chat_id"], message_id=None, user_nic=data["user_nic"],
            user_name=data["user_name"], new_text=f"{text.msg_block_airtime}",
            new_photo=None, new_file=None, keyboard=kb, status=False) - Вызов сообщения без попытки изменить прошлое сообщение, без фото и файлов, а также без удаления сообщения от пользователя
		- await utils.send_message(bot=bot, db=db, chat_id=data["chat_id"], message_id=None, user_nic=data["user_nic"],
            user_name=data["user_name"], new_text=f"{text.msg_block_airtime_divepool_two}",
            new_photo=text.img_block_airtime_divepool_two, new_file=None, keyboard=kb, status=True) - Вызов сообщения с попыткой изменить прошлое сообщение, с отправкой картинки, а также без удаления сообщения от пользователя
	
Структура бота:
	msg: ["/start"] - Приветственное сообщение
	msg: ["/info"] - Тайное сообщение о разработке бота
	clc: ("menu") - Главное меню бота
		("airtime") - Меню с данными по аэротрубе
			("airtime_double") - Дублированное меню с данными по аэротрубе 
			("airtime_divepool") - Меню с дайвпулами
				("airtime_divepool_double") - Дублированное меню с дайвпулами
				("airtime_divepool_two") - Дайвпулы 2ки
				("airtime_divepool_four") - Дайвпулы 4ки
					("airtime_divepool_four_0") - Первое фото 
					("airtime_divepool_four_0_double") - Дублированное первое фото
					("airtime_divepool_four_1") - Второе фото
					("airtime_divepool_four_2") - Третье фото
					("airtime_divepool_four_3") - Четвертое фото
				("airtime_divepool_eight") - Дайвпулы 8ки
			("airtime_ga4") - Меню с правилами ГА4
			("airtime_test") - Меню с ссылками на тесты
			("airtime_first") - Меню с обучением при 1ом полете
			("airtime_apps") - Меню с полезными приложениями
			("airtime_equipment") - Меню с описанием снаряжение для полетов
			("airtime_buy") - Меню с ссылками где кпуить снаряжение
			("airtime_locations") - Меню с геопозицией где проходят занятия
		("jumping") - Меню с данными по прыжкам
			("jumping_double") - Дублированное меню с прыжками
			("jumping_aff") - Первый файл
				("jumping_aff_double") - Дублированный первый файл
				("jumping_aff_1") - Второй файл
			("jumping_forester") - Меню с данными по системе "Лесник"
			("jumping_install") - Пособие по укладке парашюта
			("jumping_piloting") - Пособие по пилотированию парашюта
			("jumping_special") - Карта особых случаев
			("jumping_refusals") - Карта отказов
			("jumping_equipment") - Список снаряжения для прыжков
			("jumping_documents") - Список документов для прыжков
			("jumping_category") - Список категорий подготовки парашютиста
			("jumping_more") - Меню с дополнительными данными
				("jumping_more_double") - Дублированное меню с дополнительными данными
				("jumping_more_start") - Номера стартов DZ
				("jumping_more_maps") - Карта DZ
				("jumping_more_watch") - Пособие по осмотру системы
				("jumping_more_insurance") - Оформление страховки
		("competitions") - Меню с данными о соревнованиях
			("competitions_double") - Дублированное меню с данными о соревнованиях
			("competitions_flycontest") - Ссылка на Flycontest
			("competitions_rules") - Список правил
			("competitions_standards") - Список нормативов
			("competitions_calendar") - Календарь соревнований
			("competitions_rusada") - Меню с данными РУСАДА
		("additionally") - Меню с дополнительными данными
			("additionally_double") - Дублированное меню с дополнительными данными
			("additionally_aerodynamics") - Пособие по аэродинамике
			("additionally_maps") - Карта загрузки
			("additionally_weather") - Приложения для отслеживания погоды
		("about") - Меню с данными о клубе
			("about_double") - Дублированное меню с данными о клубе
			("about_director") - Данные о руководители клуба
			("about_trainer") - Данные о 1ом тренере (Николай Шапарин)
				("about_trainer_double") - Данные о 1ом тренере (Николай Шапарин)
				("about_trainer_1") - Данные о 2ом тренере (Наталья Шапарина)
				("about_trainer_2") - Данные о 3ем тренера (Анна Толстопятова)
			("about_mission") - Миссия клуба
			("about_contacts") - Контакты для связи
	
	
	
Серверное оборудование:
Интерпретатор: Python3.12
Библиотеки:
	import aiogram  # Библиотека для работы с Telegram-API
	import json  # Библиотека для работы с JSON-данными (чтение, запись, сериализация и десериализация).
	import asyncio  # Библиотека для работы с асинхронными функциями и управления асинхронными задачами.
	import pymysql  # Библиотека для подключения и работы с базами данных MySQL через Python.
	import os  # Библиотека для работы с файловой системой и взаимодействия с операционной средой.
	import datetime  # Библиотека для работы с датой и временем (создание, форматирование, вычисления).
	import time  # Библиотека для работы со временем (измерение времени, задержки, обработка временных меток).
	import threading  # Библиотека для работы с многопоточностью и параллельным выполнением задач.
	import socket  # Библиотека для отправки TCP/UDP запросов.
Демоны:
	- sudo systemctl status airborne.service  # Получение статуса демона
	- sudo systemctl start airborne.service  # Запуск исполняемого файла
	- sudo systemctl enable airborne.service  # Включение демона
	- sudo systemctl daemon-reload  # Обновление файлов демона
	- sudo nano /usr/lib/systemd/system/airborne.service  # Файл демона для данного бота
	НАСТРОЙКА ДЕМОНА:
		[Unit]
		Description=AirBorneClub-Telegram
		After=multi-user.target
		After=network.target
		After=syslog.target

		[Service]
		User=kkleytt
		WorkingDirectory=/home/kkleytt/bots/airborne
		ExecStart=/usr/bin/python3.12 /home/kkleytt/bots/airborne/bot.py
		Restart=always

		[Install]
		WantedBy=multi-user.target
		
Настройки config.json:
"TOKEN": "TOKEN",  # Токен Telegram-бота
"DATABASE": {  # Настройки БД
	"SETTINGS": {  # Настройки подключения
		"IP": "192.168.0.1",  # IP-адрес для подключения к БД
		"PORT": 3306,  # Порт для подключения к БД
		"NAME": "AirborneClub_TelegramAPI",  # Название таблицы в БД
		"TIMEOUT": 60,  # Время для подключения
		"CHECK_PING": 900,  # Таймер для проверки ping до БД
		"RE_CONNECT": 3600,  # Тамйер для переподключения к БД
		"STANDARD_USER": "ADMIN"  # Стандартный пользователь для подключения к БД
	},
	"USERS": {  # Список пользователей
		"USER": {  # Данные обычного пользователя
			"LOGIN": "user_login",  # Логин обычного пользователя
			"PASSWORD": "user_pass"  # Пароль обычного пользователя
        },
		"ADMIN": {  # Данные root пользователя
			"LOGIN": "admin_login",  # Логин root пользователя
			"PASSWORD": "admin_password"  # Пароль root пользователя
        }
    }
},
"LOG_FILE": "2025-02-22-data.log",  # Название лог-файла
"LOGING_DATA": "True",  # Разрешение на логирование данных
"ADMIN_USERS": [],  # Список администраторов бота
"VERSION_BOT": "1.1-alpha",  # Версия бота
"DATA_CREATE": "16.02.2025",  # Дата создания / обновления бота
"CREATORS": {  # Список создателей
	"PROGRAMMER": "Kkleytt",  # Разработчик
	"WRITER": "annatlsp",  # Тех писатель
	"TESTER": "llikht",  # Тестировщик
	"IDEA_AUTHOR": "annatlsp",  # Автор идеи
	"PROJECT_MANAGER": "airborneclub"  # Руководитель
},
"ADMIN": 685865278,  # ID пользователя для отправки оповещений о ошибках
"SEND_ALL_NOTIFICATIONS": "False",  # Отправлять все оповещения
"SEND_CRITICAL_NOTIFICATIONS": "True"  # Отправлять только КРИТ оповещения


База данных (MySQL):
	chat_id[INT] - Идентификатор чата, где бот общается с пользователем
	message_id[INT] - Идентификатор последнего сообщения от бота
	user_nic[TEXT] - Ник-нейм пользователя без @ в начала. Kkleytt, llikht и тд.
	user_name[TEXT] - Полное имя пользователя. Фёдор Корниецкий, Лихторенко Олеся и тд.
	last_time[TEXT] - Последнее время взаимодействия с ботом в формате YYYY:MM:DD:HH:MM (ГОД:МЕСЯЦ:ДЕНЬ:ЧАС:МИНУТА)