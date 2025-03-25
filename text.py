from aiogram.types import InlineKeyboardButton


# Блок с "Меню"
msg_block_zero = """*Airborne Club*"""
msg_block_hello = """\\! Данный бот является базой знаний парашютного клуба [*Airborne Club*](https://t.me/airborneteam)🛩️\\.  
Здесь ты можешь найти обучающий материал по аэротрубным дисциплинам, полетам и прыжкам\\."""
key_block_hello = [
    [InlineKeyboardButton(text="Меню", callback_data="menu")],
    [InlineKeyboardButton(text="О нас", callback_data="about")]]
key_block_info = [
    [InlineKeyboardButton(text="Меню", callback_data="menu")],
    [InlineKeyboardButton(text="О нас", callback_data="about")]]

msg_block_menu = """📍 *Главное меню*"""
key_block_menu = [
    [InlineKeyboardButton(text="Аэротруба", callback_data="airtime")],
    [InlineKeyboardButton(text="Прыжки", callback_data="jumping")],
    [InlineKeyboardButton(text="Соревнования", callback_data="competitions")],
    [InlineKeyboardButton(text="Дополнительно", callback_data="additionally")],
    [InlineKeyboardButton(text="О нас", callback_data="about")]
]
key_block_menu_admin = [
    [InlineKeyboardButton(text="Аэротруба", callback_data="airtime")],
    [InlineKeyboardButton(text="Прыжки", callback_data="jumping")],
    [InlineKeyboardButton(text="Соревнования", callback_data="competitions")],
    [InlineKeyboardButton(text="Дополнительно", callback_data="additionally")],
    [InlineKeyboardButton(text="О нас", callback_data="about")],
    [InlineKeyboardButton(text="Администрирование", callback_data="admin_panel")]
]

# Блок с "Аэротруба"
msg_block_airtime = """📍 *Аэротруба*"""
key_block_airtime = [
    [InlineKeyboardButton(text="Дайвпул", callback_data="airtime_divepool"),
     InlineKeyboardButton(text="Правила ГА4", callback_data="airtime_ga4")],
    [InlineKeyboardButton(text="Тестирование", callback_data="airtime_test"),
     InlineKeyboardButton(text="1й полет", callback_data="airtime_first")],
    [InlineKeyboardButton(text="Приложения", callback_data="airtime_apps"),
     InlineKeyboardButton(text="Снаряжение", callback_data="airtime_equipment")],
    [InlineKeyboardButton(text="Покупка", callback_data="airtime_buy"),
     InlineKeyboardButton(text="Занятия", callback_data="airtime_locations")],
    [InlineKeyboardButton(text="Назад", callback_data="menu")]]

msg_block_airtime_divepool = """📍 *Дайвпул*"""
key_block_airtime_divepool = [
    [InlineKeyboardButton(text="2ки", callback_data="airtime_divepool_two"),
     InlineKeyboardButton(text="4ки", callback_data="airtime_divepool_four"),
     InlineKeyboardButton(text="8ки", callback_data="airtime_divepool_eight")],
    [InlineKeyboardButton(text="Назад", callback_data="airtime")]]

msg_block_airtime_divepool_two = """📍 *Дайвпул* 2ки"""
key_block_airtime_divepool_two = [[InlineKeyboardButton(text="Назад", callback_data="airtime_divepool_double")]]
img_block_airtime_divepool_two = "img_block_airtime_divepool_two.jpg"

msg_block_airtime_divepool_four_0 = """📍 *Дайвпул* 4ки"""
key_block_airtime_divepool_four_0 = [
    [InlineKeyboardButton(text="➡️", callback_data="airtime_divepool_four_1")],
    [InlineKeyboardButton(text="Назад", callback_data="airtime_divepool_double")]]
img_block_airtime_divepool_four_0 = "img_block_airtime_divepool_four_0.jpg"

msg_block_airtime_divepool_four_1 = """📍 *Дайвпул* 4ки"""
key_block_airtime_divepool_four_1 = [
    [InlineKeyboardButton(text="⬅️", callback_data="airtime_divepool_four_double"),
     InlineKeyboardButton(text="➡️", callback_data="airtime_divepool_four_2")],
    [InlineKeyboardButton(text="Назад", callback_data="airtime_divepool_double")]]
img_block_airtime_divepool_four_1 = "img_block_airtime_divepool_four_1.jpg"

msg_block_airtime_divepool_four_2 = """📍 *Дайвпул* 4ки"""
key_block_airtime_divepool_four_2 = [
    [InlineKeyboardButton(text="⬅️", callback_data="airtime_divepool_four_1"),
     InlineKeyboardButton(text="➡️", callback_data="airtime_divepool_four_3")],
    [InlineKeyboardButton(text="Назад", callback_data="airtime_divepool_double")]
]
img_block_airtime_divepool_four_2 = "img_block_airtime_divepool_four_2.jpg"

msg_block_airtime_divepool_four_3 = """📍 *Дайвпул* 4ки"""
key_block_airtime_divepool_four_3 = [
    [InlineKeyboardButton(text="⬅️", callback_data="airtime_divepool_four_2")],
    [InlineKeyboardButton(text="Назад", callback_data="airtime_divepool_double")]]
img_block_airtime_divepool_four_3 = "img_block_airtime_divepool_four_3.jpg"

msg_block_airtime_divepool_eight = """📍 *Дайвпул* 8ки"""
key_block_airtime_divepool_eight = [[InlineKeyboardButton(text="Назад", callback_data="airtime_divepool_double")]]
file_block_airtime_divepool_eight = "file_block_airtime_divepool_eight.pdf"

msg_block_airtime_ga4 = """📍 *Правила ГА4*"""
key_block_airtime_ga4 = [[InlineKeyboardButton(text="Назад", callback_data="airtime_double")]]
file_block_airtime_ga4 = "file_block_airtime_ga4.pdf"

msg_block_airtime_test = """📍 *Тестирование*\n\n· [*Алфавит*](https://madte.st/liA2mOcD)\n· [*Блоки интерн класса*](https://madte.st/C5cU9E55)"""
key_block_airtime_test = [[InlineKeyboardButton(text="Назад", callback_data="airtime")]]

msg_block_airtime_first = """📍 *1й Полет\\. Видео\\-инструкция*\n\n[*YouTube*](https://youtube.com/playlist?list=PLSQN5zMlQEkujothhgPHAL2DznN3ryp-q&si=v5-aZlF0-L8sykEo)"""
key_block_airtime_first = [[InlineKeyboardButton(text="Назад", callback_data="airtime")]]

msg_block_airtime_apps = """📍 *Приложения*\n\n· [*iPhone*](https://apps.apple.com/ru/app/4-way-coach/id477045460)\n· [*Android*](https://play.google.com/store/apps/details?id=com.fsninja.fsninja)"""
key_block_airtime_apps = [[InlineKeyboardButton(text="Назад", callback_data="airtime")]]

msg_block_airtime_equipment = """📍 *Снаряжение для полетов*"""
key_block_airtime_equipment = [[InlineKeyboardButton(text="Назад", callback_data="airtime_double")]]
file_block_airtime_equipment = "file_block_airtime_equipment.pdf"

msg_block_airtime_buy = """
📍 *Снаряжение для полетов*\n
Комбинезон, пояс для грузов, груза \\- [*Парашоп Парсьют*](https://yandex.ru/maps/org/parashop/1008660324?si=12x7y6rvu49035raz9496xz164)\n
Шлем Клауд \\- [*Юрий Жарков*](89031359380) \\- \\+7 \\(903\\) 135\\-93\\-80\n
__Чтобы получить скидку, сообщите что пришли от *Шапарина Юрия*__ 
"""
key_block_airtime_buy = [[InlineKeyboardButton(text="Назад", callback_data="airtime")]]

msg_block_airtime_locations = """
📍 *Места проведения занятий*\n
Полеты \\- [*Freezone*](https://yandex.ru/maps/org/freezone/1196764854?si=12x7y6rvu49035raz9496xz164)\n
Накатка \\- [*Клуб Десантник*](https://yandex.ru/maps/org/sportivny_klub_desantnik/1039229071?si=12x7y6rvu49035raz9496xz164)
Код от подъезда \\- *7к1988* 
"""
key_block_airtime_locations = [[InlineKeyboardButton(text="Назад", callback_data="airtime")]]


# Блок с "Прыжки"
msg_block_jumping = """📍 *Прыжки*"""
key_block_jumping = [
    [InlineKeyboardButton(text="AFF", callback_data="jumping_aff"),
     InlineKeyboardButton(text="Лесник", callback_data="jumping_forester")],
    [InlineKeyboardButton(text="Укладка парашюта", callback_data="jumping_install"),
     InlineKeyboardButton(text="Пилотирование", callback_data="jumping_piloting")],
    [InlineKeyboardButton(text="Особые случаи", callback_data="jumping_special"),
     InlineKeyboardButton(text="Отказы", callback_data="jumping_refusals")],
    [InlineKeyboardButton(text="Снаряжение", callback_data="jumping_equipment"),
     InlineKeyboardButton(text="Документы", callback_data="jumping_documents")],
    [InlineKeyboardButton(text="Категории допуска", callback_data="jumping_category"),
     InlineKeyboardButton(text="Дополнительно", callback_data="jumping_more")],
    [InlineKeyboardButton(text="Назад", callback_data="menu")]
]

msg_block_jumping_aff_0 = """📍 *AFF методичка*"""
key_block_jumping_aff_0 = [
    [InlineKeyboardButton(text="➡️", callback_data="jumping_aff_1")],
    [InlineKeyboardButton(text="Назад", callback_data="jumping_double")]]
file_block_jumping_aff_0 = "file_block_jumping_aff_0.pdf"
msg_block_jumping_aff_1 = """📍 *AFF методичка*"""
key_block_jumping_aff_1 = [
    [InlineKeyboardButton(text="⬅️", callback_data="jumping_aff_double")],
    [InlineKeyboardButton(text="Назад", callback_data="jumping_double")]]
file_block_jumping_aff_1 = "file_block_jumping_aff_1.pdf"

msg_block_jumping_forester = """📍 *Лесник*"""
key_block_jumping_forester = [[InlineKeyboardButton(text="Назад", callback_data="jumping")]]
file_block_jumping_forester = "file_block_jumping_forester.pdf"

msg_block_jumping_install = """📍 *Укладка парашюта\\. Пособие*\n\n[*YouTube*](https://youtu.be/ytssh2BVZrI?si=f0AhgLpbLAzvm7OH)"""
key_block_jumping_install = [[InlineKeyboardButton(text="Назад", callback_data="jumping")]]

msg_block_jumping_piloting = """📍 *Пилотирование\\. Пособие*"""
key_block_jumping_piloting = [[InlineKeyboardButton(text="Назад", callback_data="jumping_double")]]
file_block_jumping_piloting = "file_block_jumping_piloting.pdf"

msg_block_jumping_special = """📍 *Карта особых случаев*"""
key_block_jumping_special = [[InlineKeyboardButton(text="Назад", callback_data="jumping_double")]]
file_block_jumping_special = "file_block_jumping_special.pdf"

msg_block_jumping_refusals = """📍 *Карта отказов*"""
key_block_jumping_refusals = [[InlineKeyboardButton(text="Назад", callback_data="jumping_double")]]
img_block_jumping_refusals = "img_block_jumping_refusals.jpg"

msg_block_jumping_equipment = """📍 *Снаряжение для прыжков*"""
key_block_jumping_equipment = [[InlineKeyboardButton(text="Назад", callback_data="jumping")]]

msg_block_jumping_documents = """📍 *Документы для прыжков*\n\n· Страховка\n· Справка от врача, что ограничений для прыжков нет, либо ВЛЭК для парашютистов"""
key_block_jumping_documents = [[InlineKeyboardButton(text="Назад", callback_data="jumping")]]

msg_block_jumping_category = """📍 *Категории допуска к прыжкам*"""
key_block_jumping_category = [
    [InlineKeyboardButton(text="A", callback_data="jumping_category_a"),
     InlineKeyboardButton(text="B", callback_data="jumping_category_b")],
    [InlineKeyboardButton(text="C", callback_data="jumping_category_c"),
     InlineKeyboardButton(text="D", callback_data="jumping_category_d")],
    [InlineKeyboardButton(text="Назад", callback_data="jumping")]
]

msg_block_jumping_more = """📍 *Дополнительно*"""
key_block_jumping_more = [
    [InlineKeyboardButton(text="Номер старта DZ", callback_data="jumping_more_start"),
     InlineKeyboardButton(text="Карта DZ", callback_data="jumping_more_maps")],
    [InlineKeyboardButton(text="Осмотр системы", callback_data="jumping_more_watch"),
     InlineKeyboardButton(text="Страховка", callback_data="jumping_more_insurance")],
    [InlineKeyboardButton(text="Назад", callback_data="jumping")]
]

msg_block_jumping_more_start = """📍 *Номера стартов всех аэродромов*\n
· _Орешково_ \\- \\+7 \\(903\\) 136\\-09\\-96
· _Ватулино_ \\- \\+7 \\(926\\) 166\\-83\\-19
· _Пущино_ \\- \\+7 \\(964\\) 565\\-61\\-63
· _Коломна_ \\- \\+7 \\(964\\) 726\\-55\\-24
"""
key_block_jumping_more_start = [[InlineKeyboardButton(text="Назад", callback_data="jumping_more")]]

msg_block_jumping_more_maps = """
📍 *Карты DZ*\n
· [*Орешково*](https://yandex.ru/maps/?whatshere%5Bzoom%5D=15&whatshere%5Bpoint%5D=36.068145,54.469801&si=12x7y6rvu49035raz9496xz164) \\- 54\\.469801,36\\.068145
· [*Ватулино*](https://yandex.ru/maps/?whatshere%5Bzoom%5D=17&whatshere%5Bpoint%5D=36.142077,55.662695&si=12x7y6rvu49035raz9496xz164) \\- 55\\.662695,36\\.142077
· [*Коломна*](https://yandex.ru/maps/?whatshere%5Bzoom%5D=16&whatshere%5Bpoint%5D=38.918629,55.089952&si=12x7y6rvu49035raz9496xz164) \\- 55\\.089952,38\\.918629
· [*Пущино*](https://yandex.ru/maps/?whatshere%5Bzoom%5D=17&whatshere%5Bpoint%5D=37.643614,54.787432&si=12x7y6rvu49035raz9496xz164) \\- 54\\.787432,37\\.643614
· [*Волосово*](https://yandex.ru/maps/?whatshere%5Bzoom%5D=17&whatshere%5Bpoint%5D=37.454770,55.067008&si=12x7y6rvu49035raz9496xz164) \\- 55\\.067008,37\\.454770
"""
key_block_jumping_more_maps = [[InlineKeyboardButton(text="Назад", callback_data="jumping_more")]]

msg_block_jumping_more_watch = """📍 *Осмотр системы*"""
key_block_jumping_more_watch = [[InlineKeyboardButton(text="Назад", callback_data="jumping_more_double")]]
img_block_jumping_more_watch = "img_block_jumping_more_watch.jpg"

msg_block_jumping_more_insurance = """📍 *Получение страховки*\n\n[*Ингосстрах*](https://www.ingos.ru/life/neschastnyj-sluchaj/calc)"""
key_block_jumping_more_insurance = [[InlineKeyboardButton(text="Назад", callback_data="jumping_more")]]

# Блок с "Соревнования" и дочерние блоки: "Флайконтест", "Правила", "Нормативы", "Календарь"
msg_block_competitions = """📍 *Соревнования*"""
key_block_competitions = [
    [InlineKeyboardButton(text="Флайконтест", callback_data="competitions_flycontest"),
     InlineKeyboardButton(text="Правила", callback_data="competitions_rules")],
    [InlineKeyboardButton(text="Нормативы", callback_data="competitions_standards"),
     InlineKeyboardButton(text="Календарь", callback_data="competitions_calendar")],
    [InlineKeyboardButton(text="РУСАДА", callback_data="competitions_rusada")],
    [InlineKeyboardButton(text="Назад", callback_data="menu")]
]

msg_block_competitions_flycontest = """📍 *Флайконтест*\n\n[*FlyContest*](https://flycontest.ru)"""
key_block_competitions_flycontest = [[InlineKeyboardButton(text="Назад", callback_data="competitions")]]

msg_block_competitions_rules = """📍 *Правила парашютного спорта*"""
key_block_competitions_rules = [[InlineKeyboardButton(text="Назад", callback_data="competitions_double")]]
file_block_competitions_rules = "file_block_competitions_rules.pdf"

msg_block_competitions_standards = """📍 *Нормативы*"""
key_block_competitions_standards = [[InlineKeyboardButton(text="Назад", callback_data="competitions_double")]]
img_block_competitions_standards = "img_block_competitions_standards.jpg"

msg_block_competitions_calendar = """📍 *Календарь*\n\n[*Календарь соревнований 2025г*](https://teamup.com/ksd2i6qcd3iauxo94t)"""
key_block_competitions_calendar = [[InlineKeyboardButton(text="Назад", callback_data="competitions")]]

msg_block_competitions_rusada = """📍 *РУСАДА*\n\n[*Официальный сайт*](https://course.rusada.ru/#login-popup)"""
key_block_competitions_rusada = [[InlineKeyboardButton(text="Назад", callback_data="competitions")]]

# Блок с "Дополнительно" с дочерними блоками: "Аэродинамика", "Карта загрузки"
msg_block_additionally = """📍 *Дополнительно*"""
key_block_additionally = [
    [InlineKeyboardButton(text="Аэродинамика", callback_data="additionally_aerodynamics"),
     InlineKeyboardButton(text="Карта загрузки", callback_data="additionally_maps")],
    [InlineKeyboardButton(text="Карта погоды", callback_data="additionally_weather")],
    [InlineKeyboardButton(text="Назад", callback_data="menu")]
]
msg_block_additionally_aerodynamics = """📍 *Основы аэродинамики*"""
key_block_additionally_aerodynamics = [[InlineKeyboardButton(text="Назад", callback_data="additionally_double")]]
file_block_additionally_aerodynamics = "file_block_additionally_aerodynamics.pdf"

msg_block_additionally_maps = """📍 *Карта загрузки*"""
key_block_additionally_maps = [[InlineKeyboardButton(text="Назад", callback_data="additionally_double")]]
file_block_additionally_maps = "file_block_additionally_maps.pdf"

msg_block_additionally_weather = """📍 *Карта погоды*\n\n· [*Погодный радар*](https://goo.su/FGf3)\n· [*Погода, ветер и волны*](https://goo.su/Jjw7CE)"""
key_block_additionally_weather = [[InlineKeyboardButton(text="Назад", callback_data="additionally")]]


# Блок с "О нас"
msg_block_about = """📍 *О нас*"""
key_block_about = [
    [InlineKeyboardButton(text="Руководство", callback_data="about_director"),
     InlineKeyboardButton(text="Тренеры", callback_data="about_trainer")],
    [InlineKeyboardButton(text="Миссия", callback_data="about_mission"),
     InlineKeyboardButton(text="Контакты", callback_data="about_contacts")],
    [InlineKeyboardButton(text="Назад", callback_data="menu")],
]

msg_block_about_director = """
📍 *Руководство*\n
*Шапарин Юрий Юрьевич*\n\nПрезидент клуба *«Десантник»*, главный тренер школы *Airborne club*\\.\n
Летчик\\-инструктор\\-парашютист\\. Основал спортивный клуб *«Десантник»* в декабре 1987 года\\.  
Более *35 лет* занимается подготовкой парашютистов и воспитанием подрастающего поколения\\.
"""
key_block_about_director = [[InlineKeyboardButton(text="Назад", callback_data="about_double")]]
img_block_about_director = "img_block_about_director.jpg"

msg_block_about_mission = (
    "📍 *Миссия*\n\n"
    "Наша миссия заключается в том, чтобы помочь людям\\:\n"
    "· развивать свои навыки в парашютной групповой акробатике,\n · учить уверенности,\n · решительности,\n · командной работе\\.\n\n"
    "Открывать для наших учеников уникальные возможности, которые предоставляет парашютное сообщество\\. "
    "Через обучение стремимся вдохновлять, мотивировать и делать людей счастливыми, "
    "которые будут достигать новые высоты и преодолевать личные ограничения\\.\n\n"
    "Почему люди приходят в парашютный спорт\\? Это может быть вызвано разными факторами\\:\n\n"
    "🔥 *Адреналин и свобода*\\: Это опыт, который невозможно получить в повседневной жизни\\. "
    "Парашютный спорт дарит невероятное ощущение полета и свободы, которое привлекает людей, "
    "стремящихся испытать новые эмоции\\.\n\n"
    "🪂 *Саморазвитие и преодоление страха*\\: Прыжок с парашютом \\— это серьезный вызов для психики, "
    "и успешное преодоление этого страха дает чувство гордости и уверенности в себе\\. "
    "Это помогает людям стать смелее в жизни в целом\\.\n\n"
    "🥰 *Командная работа*\\: В групповой акробатике важна синхронность и доверие между партнерами\\. "
    "Это обучение командной работе, что полезно не только в спорте, но и в жизни\\.\n\n"
    "💪 *Чисто физическое наслаждение*\\: Это спортивная активность, которая сочетает физическую нагрузку, "
    "ловкость и координацию движений, что также привлекает людей, интересующихся физическим развитием\\.\n\n"
    "🏆 *Достижение целей*\\: Каждое достижение в парашютном спорте, будь то успешный прыжок или завершение тренировки, "
    "приносит чувство выполненного долга\\. Люди, стремящиеся к личностному росту и новым достижениям, часто выбирают этот спорт\\."
)

key_block_about_mission = [[InlineKeyboardButton(text="Назад", callback_data="about")]]

msg_block_about_contacts = """
📍 *Контакты*\n
*Соц сети*\\:
· 🟦 [*VK*](https://vk.com/airborne_club)
· 🟦 [*VK*](https://vk.com/airborneclub)
· 🟥 [*YouTube*](https://youtube.com/@airborne_club?si=x70-5ydfSVnsc7gF)
· 🟧 [*Instagram*](https://www.instagram.com/airborneclub_team?igsh=amttenp2Zndjcngy&utm_source=qr)
· 🟦 [*Telegram*](https://t.me/addlist/h6E5GZaRWiIwNThi)
· 🟩 [*WhatsApp*](https://chat.whatsapp.com/BBD7xJocCcT5vHYutQ294J)\n
*Контакты*\\:
· *Шапарин Юрий Юрьевич* \\- 89031360996
· *Шапарин Николай Юрьевич* \\- 89651725972
"""
key_block_about_contacts = [[InlineKeyboardButton(text="Назад", callback_data="about")]]

key_block_about_trainer_0 = [
    [InlineKeyboardButton(text="➡️", callback_data="about_trainer_1")],
    [InlineKeyboardButton(text="Назад", callback_data="about_double")]
]
msg_block_about_trainer_0 = """
📍 *Тренеры*\n\n*Шапарин Николай Юрьевич*\n_Старший тренер_\n\n*Мастер спорта*
· Занимается парашютным спортом с *2010* года и групповой акробатикой с *2017* года\\. 
· Тренирует с *2019* года\\.  
· Инструктор парашютно\\-десантной подготовки с *2022* года\\.
"""
img_block_about_trainer_0 = "img_block_about_trainer_0.jpg"

key_block_about_trainer_1 = [
    [InlineKeyboardButton(text="⬅️", callback_data="about_trainer_double"),
     InlineKeyboardButton(text="➡️", callback_data="about_trainer_2"),],
    [InlineKeyboardButton(text="Назад", callback_data="about_double")]
]
msg_block_about_trainer_1 = """
📍 *Тренеры*\n\n*Шапарина Наталья Юрьевна*\n_Тренер_\n\n*Мастер спорта*
· Занимается парашютным спортом с *2010* года и групповой акробатикой с *2017* года\\. 
· Тренирует с *2019* года\\.
"""
img_block_about_trainer_1 = "img_block_about_trainer_1.jpg"

key_block_about_trainer_2 = [
    [InlineKeyboardButton(text="⬅️", callback_data="about_trainer_1")],
    [InlineKeyboardButton(text="Назад", callback_data="about_double")]
]
msg_block_about_trainer_2 = """
📍 *Тренеры*\n\n*Толстопятова Анна Сергеевна*\n_Тренер_\n\n*Мастер спорта*
· Занимается групповой акробатикой с *2018* года\\. 
· С *2019* начала свою тренерскую деятельность, в том числе подготовку самых маленьких спортсменов от *2х* лет\\.
"""
img_block_about_trainer_2 = "img_block_about_trainer_2.jpg"
