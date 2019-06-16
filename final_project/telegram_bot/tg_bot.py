import telebot
from peewee import *

import conf
from model import Anecdote
from chat_state import ChatState


telebot.apihelper.proxy = {'https': 'socks5h://geek:socks@t.geekclass.ru:7777'}
bot = telebot.TeleBot(conf.ACCESS_TOKEN)
db = SqliteDatabase('anecdotes.db')
chat_states = {}


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, conf.WELCOME_MESSAGE,
                     parse_mode='Markdown')


def send_anecdotes(chat_id):
    global chat_states
    anecs = list(Anecdote.select().order_by(fn.Random()).limit(2))
    chat_states[chat_id].last_anecs = anecs

    for i, anec in enumerate(anecs):
        reply_text = '\n\n'.join([f'<b>АНЕКДОТ {i + 1}</b>', anec.text])
        bot.send_message(chat_id, reply_text, parse_mode='HTML')

    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2,
                                                 resize_keyboard=True,
                                                 one_time_keyboard=True)
    button_first = telebot.types.KeyboardButton(chr(0x261D) + 'Первый')
    button_second = telebot.types.KeyboardButton(chr(0x270C) + 'Второй')
    not_anec_msg = chr(0x1F612) + 'Что-то из этого вообще не анек'
    button_not_anec = telebot.types.KeyboardButton(not_anec_msg)
    keyboard.add(button_first, button_second, button_not_anec)
    bot.send_message(chat_id,
                     'Какой из этих анеков набрал больше лайков?',
                     reply_markup=keyboard)


@bot.message_handler(commands=['play'])
def start_play(message):
    global chat_states
    chat_states[message.chat.id] = ChatState(message.chat.id)
    send_anecdotes(message.chat.id)


@bot.message_handler(func=lambda x: x.text == chr(0x261D) + 'Первый')
def first_is_chosen(message):
    global chat_states
    try:
        first_likes = chat_states[message.chat.id].last_anecs[0].likes
        second_likes = chat_states[message.chat.id].last_anecs[1].likes
    except KeyError:
        bot.reply_to(message, 'Что-то пошло не так. Нажмите /play еще раз')
        return
    if first_likes >= second_likes:
        chat_states[message.chat.id].won += 1
        msg = (f'Верно! Первый анек набрал {first_likes} лайков, '
               f'а второй – {second_likes}')
    else:
        chat_states[message.chat.id].lost += 1
        msg = (f'Не-а. Первый анек набрал {first_likes} лайков, '
               f'а второй – {second_likes}')

    bot.send_message(message.chat.id, msg)
    send_anecdotes(message.chat.id)


@bot.message_handler(func=lambda x: x.text == chr(0x270C) + 'Второй')
def second_is_chosen(message):
    global chat_states
    try:
        first_likes = chat_states[message.chat.id].last_anecs[0].likes
        second_likes = chat_states[message.chat.id].last_anecs[1].likes
    except KeyError:
        bot.reply_to(message, 'Что-то пошло не так. Нажмите /play еще раз')
        return None
    if second_likes >= first_likes:
        chat_states[message.chat.id].won += 1
        msg = (f'Верно! Второй анек набрал {second_likes} лайков, '
               f'а первый – {first_likes}')
    else:
        chat_states[message.chat.id].lost += 1
        msg = (f'Не-а. Второй анек набрал {second_likes} лайков, '
               f'а первый – {first_likes}')

    bot.send_message(message.chat.id, msg)
    send_anecdotes(message.chat.id)


@bot.message_handler(func=lambda x:
                     x.text == chr(0x1F612) + 'Что-то из этого вообще не анек')
def not_anec(message):
    bot.send_message(message.chat.id, 'Ок, вот другие посты!')
    send_anecdotes(message.chat.id)


@bot.message_handler(commands=['stop'])
def show_stats(message):
    chat_id = message.chat.id
    if (chat_states[chat_id].won % 10 in range(0, 2) or
        chat_states[chat_id].won % 10 in range(5, 10)):
        word_form = 'раз'
    elif chat_states[chat_id].won % 10 in range(2, 5):
        word_form = 'раза'
    msg = (f'Ты угадал(а) {chat_states[chat_id].won} раз '
           f'и ошибся(лась) {chat_states[chat_id].lost}.')
    bot.send_message(chat_id, msg)
    bot.send_message(chat_id, 'Чтобы сыграть еще раз, нажми /play')


def main():
    db.connect()
    try:
        bot.polling()
    finally:
        db.close()

if __name__ == '__main__':
    main()
