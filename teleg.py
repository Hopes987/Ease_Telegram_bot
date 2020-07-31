import telebot
import sqlite3
from datetime import datetime
import time
import asyncio
print("Work")

# conn = sqlite3.connect("mydatabase_2.db") # или :memory: чтобы сохранить в RAM
# cursor = conn.cursor()

# # Создание таблицы
# cursor.execute("""CREATE TABLE users(ID int, Name text, date text, status int, time_work datetime)""")

bot = telebot.TeleBot('1373601737:AAHOCuPW0kRxklH9QNe77_KHkg4twZz75vY')


def chek(mess):
    users_list = []
    conn = sqlite3.connect("mydatabase_2.db")
    cur = conn.cursor()
    for row in cur.execute("SELECT * FROM users"):
        users_list.append(row)
    for people in users_list:
        if int(people[0]) == mess:
            return True
    conn.close()

def update(upd, message, mess, name_id, name_non):
    time_w = datetime.now().date()
    conn = sqlite3.connect("mydatabase_2.db")
    cur = conn.cursor()
    if upd == True:
        send_text_upd(message)
    elif upd == None:
        if name_id == None:
            cur.execute(
                f"INSERT INTO users VALUES ({mess}, '{name_non}', '{time_w}', 0, 0)")
        else:
            cur.execute(
                f"INSERT INTO users VALUES ({mess}, '{name_id}', '{time_w}', 0 , 0)")
        conn.commit()
        send_text_u(message)
    conn.close()

def change_status(name_id):
    conn = sqlite3.connect("mydatabase_2.db")
    cursor = conn.cursor()
    today = datetime.today()
    sql = f"UPDATE users SET status = '1' WHERE Name = '{name_id}'"
    sql_1 = f"UPDATE users SET time_work = '{today.strftime('%Y.%m.%d.%H.%M.%S')}' WHERE Name = '{name_id}'"
    cursor.execute(sql)
    cursor.execute(sql_1)
    conn.commit()
    conn.close()

def change_status_d(name_id, message, mess):
    conn = sqlite3.connect("mydatabase_2.db")
    cursor = conn.cursor()
    fdf = datetime
    time_minus = datetime
    for row in cursor.execute("SELECT * FROM users ORDER BY time_work"):
        if row[0] == mess:
            fdf = row[4]

    if not fdf == 0:
        fdf = str(fdf)
        fdf = fdf.split(".")
        time_minus = datetime.now() - \
            datetime(int(fdf[0]), int(fdf[1]), int(
                fdf[2]), int(fdf[3]), int(fdf[4]))
    else:
        time_minus = "Не получилось!!"
    send_text_time(message, time_minus)
    sql = f"UPDATE users SET status = '0' WHERE Name = '{name_id}'"
    sql_n = f"UPDATE users SET time_work = '0' WHERE Name = '{name_id}'"
    cursor.execute(sql)
    cursor.execute(sql_n)
    conn.commit()
    conn.close()

def who_a(message):
    conn = sqlite3.connect("mydatabase_2.db")
    cursor = conn.cursor()
    for row in cursor.execute("SELECT * FROM users ORDER BY time_work"):
        if row[3] == 1:
            who = row[0]
            name = row[1]
            send_text_who(message, who, name)
    conn.close()

keyboard1 = telebot.types.ReplyKeyboardMarkup(False, False)
keyboard1.row("Я тут", 'Есть кто ?', "Уйти")
keyboard4 = telebot.types.ReplyKeyboardMarkup(False, False)
keyboard4.add('Авторизоваться')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(
        message.chat.id, 'Привет, ты написал мне /start', reply_markup=keyboard4)


@bot.message_handler(content_types=['text'])
def send_text(message):
    mess = ''
    mess = message.chat.id
    name_id = message.from_user.username
    name_non = message.from_user.first_name

    if message.text.lower() == 'авторизоваться':
        bot.send_message(
            message.chat.id, f'Секунду, идет проверка с базой', reply_markup=keyboard1)
        chek(mess)
        upd = chek(mess)
        update(upd, message, mess, name_id, name_non)
    elif message.text.lower() == 'есть кто ?' or message.text.lower() == 'есть кто':
        bot.send_message(message.chat.id, 'Вот, кто на площадке',
                         reply_markup=keyboard1)
        who_a(message)

    elif message.text.lower() == 'я тут':
        bot.send_message(message.chat.id, 'Отлично!!!!')
        bot.send_message(
            message.chat.id, 'Приятных занятий спортом', reply_markup=keyboard1)
        change_status(name_id)
    elif message.text.lower() == 'уйти':
        change_status_d(name_id, message, mess)


@bot.message_handler(content_types=['text'])
def send_text_upd(message):
    bot.send_message(message.chat.id, f'Отлично, вы в базе',
                     reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def send_text_u(message):
    bot.send_message(message.chat.id, f'Идёт регистрация')
    bot.send_message(message.chat.id, f'Отлично, вы в базе')


@bot.message_handler(content_types=['text'])
def send_text_time(message, time_minus):
    bot.send_message(message.chat.id, f'Ты занимался спортом',
                     reply_markup=keyboard1)
    bot.send_message(message.chat.id, f'{time_minus}')


@bot.message_handler(content_types=['text'])
def send_text_who(message, who, name):
    bot.send_message(message.chat.id, f'id: {who} имя аккаунта @{name}')


@bot.message_handler(content_types=['text'])
def send_text_no(message):
    bot.send_message(message.chat.id, f'ААА думал кто-то есть ? нееет')


bot.polling()
