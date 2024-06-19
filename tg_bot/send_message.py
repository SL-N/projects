import telebot
from telebot import types
import datetime
import time
import re
from user_db import check_time

def send_mes(id, h, m):
    TOKEN = '1634401190:AAFqZgHM456Jyn8AnCqzKyBP0bOjk_TIl-c'
    bot = telebot.TeleBot(TOKEN, parse_mode=None)
    time_ = datetime.time(h, m)
    b = datetime.datetime.today().time()
    while b.hour != time_.hour or (b.hour == time_.hour and b.minute != time_.minute):
        time.sleep(60)
        b = datetime.datetime.today().time()
    markup = types.ReplyKeyboardMarkup()
    iteam = types.KeyboardButton('Отметиться')
    markup.add(iteam)
    bot.send_message(id, "Пришло время отметиться.", reply_markup = markup)
    time_2 = check_time(user_id = id)

    while time_ == time_2:
        time.sleep(86400)
        markup = types.ReplyKeyboardMarkup()
        iteam = types.KeyboardButton('Отметиться')
        markup.add(iteam)
        bot.send_message(id, "Пришло время отметиться.", reply_markup = markup)
        time_ = cheeck_time(user_id = id)
