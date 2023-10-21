start_non_user = """
Привет, дорогой пользователь!
Вижу, ты еще не в нашей системе!
Нажми кнопку зарегистрироваться, чтобы отправить запрос на выдачу доступа к магазину!
"""

admin_user_request = """
Привет, <b>дорогой админ!</b>
Пользователь хочет войти в систему!

Имя - <code>{name}</code>
Должность - <code>{position}</code>
ID - <code>{id}</code>
Телеграм - @{telegram_tag}

Добавляем в систему?
"""

reg_name = """
Введите ФИО:
Это необходимо для определения вас в админке
"""

reg_position = """
Введите вашу должность:
"""

reg_finish = """
Все, спасибо, мы продали ваши данные)
Шутка, мы отправили запрос админу и скоро вы получите ответ
"""

start_user = """
Привет, <code>{name}</code>!
Приветствую тебя в нашем магазине!
Твой баланс - {balance} TC
Твой ID - <code>{id}</code>
Быстрее же используй их!
"""

start_admin = """
Здравствуй, дорогой <b>{name}</b>!
Мы приветствуем вас в нашей панеле администратора!
Ждем, пока вы пополните баланс одному из ваших работников!
"""

reg_ban = """
К сожалению, админ запретил доступ тебе((
Ты в бане системы(((
"""

reg_accept = """
Тебя взяли!!!

""" + start_user

admin_user_request_accept = """
Привет, <b>дорогой админ!</b>
Пользователь добавлен в систему!

Имя - <code>{name}</code>
Должность - <code>{position}</code>
ID - <code>{id}</code>
Телеграм - @{telegram_tag}

!!! СОХРАНИ ЕГО ID, он нужен при пополнении его счета !!!
"""

admin_user_request_ban = """
Привет, <b>админ</b>!
Пользователь с ID <code>{id}</code> забанен в системе
"""

user_profile = """
Имя: <b>{name}</b>
ID: <code>{id}</code>
Баланс: <i>{balance}</i>
Должность: <b>{position}</b>
"""

product_text = """
Название: <code>{name}</code>
Описание: <b>{description}</b>
Цена: <b>{price} TC</b>
Категория <b>{category}</b>
"""