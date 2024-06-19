import telebot
import re
import time
from datetime import date
from telebot import types
from user_db import init_db, check, add_info, change_cl, stat, de, get_gr
from schedule_db import get_schedule
from send_message import send_mes

TOKEN = '1634401190:AAFqZgHM456Jyn8AnCqzKyBP0bOjk_TIl-c'
bot = telebot.TeleBot(TOKEN, parse_mode=None)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	#print(message)

	bot.reply_to(message, "Привет! ")
	init_db()
	a = check(check_id = message.from_user.id)
	if a == False:
		bot.send_message(message.chat.id, "В какой группе ты учишься?🧑🏽‍🎓 Отправь мне номер группы в формате: 11-***.")
	else:
		bot.send_message(message.chat.id, "Вы уже зарегистрированы!✅ Чтобы перейти в меню, отправьте мне сообщение 'Меню'.")


@bot.message_handler(content_types = ['text'])
def reg(message):
	if message.chat.type == 'private':
		result_gr = re.findall(r'\d{2}-\d{3}',message.text)
		result_time = re.findall(r'\d{2}:\d{2}',message.text)
		day = re.findall(r'\d{4}-\d{2}-\d{2}',message.text)
		cl = re.findall(r'-\w+',message.text)
		tx = [message.text]


		if tx == result_gr:
			markup = types.ReplyKeyboardMarkup()
			iteamY = types.KeyboardButton('Хочу')
			iteamN = types.KeyboardButton('Не хочу')
			markup.add(iteamY,iteamN)
			bot.send_message(message.chat.id, "Хочешь ли ты получать уведомления о ежедневном опросе посещаемости занятий?", reply_markup = markup)
			add_info(user_id = message.from_user.id, gr = message.text , cl = '', date = '', time = '')

		elif tx == ['Хочу'] or tx == ['Не хочу']:
			if message.text == 'Не хочу':
				bot.send_message(message.chat.id, "Хорошо, ты всегда можешь пройти опрос, отправив мне сообщение 'Меню'.")
				add_info(user_id = message.from_user.id, gr = '', cl = '', date = '', time = '' )
				de(user_id = message.from_user.id)
			else:
				bot.send_message(message.chat.id, "В какое время ты хочешь получать уведомления? Отправь мне время в формате: чч:мм (12:00, 09:30)")

		elif tx == result_time:
			error = re.findall(r':\d{2}',message.text)
			error = re.findall(r'\d{2}',error[0])
			error_ = re.findall(r'\d{2}:',message.text)
			error_ = re.findall(r'\d{2}',error_[0])
			if int(error[0]) > 59 or int(error_[0]) > 23:
				bot.send_message(message.chat.id, "Неверный формат сообщения ❌")
			else:
				de(user_id = message.from_user.id)
				add_info(user_id = message.from_user.id, gr = '', cl = '', date = '', time = message.text)
				bot.send_message(message.chat.id, "Спасибо!😊 Ты всегда можешь изменить время, отправив мне сообщение 'Меню'.")
				send_mes(message.chat.id, int(error_[0]), int(error[0]))

		elif tx == ['Меню'] or tx == ['меню']:
			markup_m = types.ReplyKeyboardMarkup()
			iteam_inter = types.KeyboardButton('Посещаемость')
			iteam_shc = types.KeyboardButton('Расписание')
			iteam_edit = types.KeyboardButton('Редактировать')
			markup_m.add(iteam_shc, iteam_inter, iteam_edit)
			bot.send_message(message.chat.id, "Вы перешли в меню.", reply_markup = markup_m)

		elif message.text == 'Посещаемость':
			markup_check = types.ReplyKeyboardMarkup()
			iteam_stat = types.KeyboardButton('Статистика')
			iteam_mark = types.KeyboardButton('Отметиться')
			iteam_menu = types.KeyboardButton('Меню')
			markup_check.add(iteam_stat, iteam_mark, iteam_menu)
			bot.send_message(message.chat.id, "Хочешь отметить пропуски или узнать статистику?", reply_markup = markup_check)

		elif message.text == 'Отметиться':
			markup_day = types.ReplyKeyboardMarkup()
			iteam_today = types.KeyboardButton('За сегодня')
			iteam_date = types.KeyboardButton('Выбрать день')
			iteam_menu = types.KeyboardButton('Меню')
			markup_day.add(iteam_today, iteam_date, iteam_menu)
			bot.send_message(message.chat.id, "За какой день ты хочешь отметиться?", reply_markup = markup_day)

		elif message.text == 'За сегодня':
			day_ = str(date.today())
			year = re.findall(r'\d{4}',day_)
			m = re.findall(r'-\d{2}-', day_)
			m = re.findall(r'\d{2}',m[0])
			d = re.findall(r'-\d{2}$', day_)
			d = re.findall(r'\d{2}',m[0])
			if m == [] or year == [] or d == []:
				bot.send_message(message.chat.id, "Неверный формат сообщения ❌")
			else:
				add_info(user_id = message.from_user.id, gr = '', cl = '', date = day_, time = '' )
				bot.reply_to(message, "Перечисли через запятую предметы, которые ты пропустил(а) в этот день.\nНачни свое сообщение со знака '-'.\nНапример, -Информатика, Физ-ра")

		elif message.text == 'Выбрать день':
			bot.send_message(message.chat.id, "Отправь мне дату в формате: гггг-мм-дд (2020-01-19)")

		elif tx == day:
			year = re.findall(r'\d{4}',message.text)
			m = re.findall(r'-\d{2}-',message.text)
			m = re.findall(r'\d{2}',m[0])
			d= re.findall(r'-\d{2}$',message.text)
			d = re.findall(r'\d{2}',m[0])
			if m == [] or year == [] or d == []:
				bot.send_message(message.chat.id, "Неверный формат сообщения ❌")
			else:
				add_info(user_id = message.from_user.id, gr = '', cl = '', date = day[0], time = '' )
				bot.reply_to(message, "Перечисли через запятую предметы, которые ты пропустил(а) в этот день.\nНачни свое сообщение со знака '-'.\nНапример, -Информатика, Физ-ра")

		elif cl != []:
			change_cl(user_id = message.from_user.id, cl = message.text)
			cl = []

		elif message.text == 'Статистика':
			mes = stat(user_id = message.from_user.id)
			if mes != {}:
				for key in mes:
					bot.send_message(message.chat.id, f'{key} ты пропустил(а):\n{mes[key]}')
			else:
				bot.send_message(message.chat.id, f'Ты еще не отмечал(а) пропуски')

		elif message.text == 'Расписание':
			markup = types.ReplyKeyboardMarkup()
			mon = types.KeyboardButton('Понедельник')
			tues = types.KeyboardButton('Вторник')
			wed = types.KeyboardButton('Среда')
			thur = types.KeyboardButton('Четверг')
			fr = types.KeyboardButton('Пятница')
			sut = types.KeyboardButton('Суббота')
			markup.add(mon, tues, wed, thur, fr, sut)
			bot.send_message(message.chat.id, "Выбери день.", reply_markup = markup)
			# cl = get_gr(message.from_user.id
			# sch = get_schedule(get_gr(message.from_user.id), message.text)
			# bot.send_message(message.chat.id, sch)

		elif message.text == 'Редактировать':
			markup = types.ReplyKeyboardMarkup()
			iteamY = types.KeyboardButton('Хочу')
			iteamN = types.KeyboardButton('Не хочу')
			markup.add(iteamY,iteamN)
			bot.send_message(message.chat.id, "Хочешь ли ты получать уведомления о ежедневном опросе посещаемости занятий?",	reply_markup = markup)

		elif message.text == 'Понедельник':
			sch = get_schedule(number = get_gr(user_id = message.from_user.id), day = message.text)
			bot.send_message(message.chat.id, sch)
		elif message.text == 'Вторник':
			sch = get_schedule(number = get_gr(user_id = message.from_user.id), day = message.text)
			bot.send_message(message.chat.id, sch)
		elif message.text == 'Среда':
			sch = get_schedule(number = get_gr(user_id = message.from_user.id), day = message.text)
			bot.send_message(message.chat.id, sch)
		elif message.text == 'Четверг':
			sch = get_schedule(number = get_gr(user_id = message.from_user.id), day = message.text)
			bot.send_message(message.chat.id, sch)
		elif message.text == 'Пятница':
			sch = get_schedule(number = get_gr(user_id = message.from_user.id), day = message.text)
			bot.send_message(message.chat.id, sch)
		elif message.text == 'Суббота':
			sch = get_schedule(number = get_gr(user_id = message.from_user.id), day = message.text)
			bot.send_message(message.chat.id, sch)

		else:
			bot.send_message(message.chat.id, "Неверный формат сообщения ❌")

bot.polling()
