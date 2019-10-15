import time
import telebot
from telebot import types
import sqlite3
from datetime import timedelta, datetime

bot = telebot.TeleBot('')

category_name =  {'1':'Events','2':'Career','3':'Sport','4':'Science','5':'Politics','6':'Education','7':'Culture','8':'Freebies'}
bot_condition = {'1': 'New user', '2': 'News as post', '3': 'Evening QMUL'}


def evening_qmul():

	database = sqlite3.connect('bot_db.sqlite')
	database.row_factory = lambda cursor, row: row[0]
	db = database.cursor()
	today = datetime.now().strftime("%d")

	today_posts = []

	db.execute("SELECT id FROM posts WHERE date_month == ? AND class_group == 1 AND p_likes=(SELECT MAX(p_likes) FROM posts WHERE date_month == ? AND class_group == 1)",
	 (today, today,))
	today_posts.append(db.fetchall())
	db.execute("SELECT id FROM posts WHERE date_month == ? AND class_group == 2 AND p_likes=(SELECT MAX(p_likes) FROM posts WHERE date_month == ? AND class_group == 2)",
	 (today, today,))
	today_posts.append(db.fetchall())
	db.execute("SELECT id FROM posts WHERE date_month == ? AND class_group == 3 AND p_likes=(SELECT MAX(p_likes) FROM posts WHERE date_month == ? AND class_group == 3)",
	 (today, today,))
	today_posts.append(db.fetchall())
	db.execute("SELECT id FROM posts WHERE date_month == ? AND class_group == 4 AND p_likes=(SELECT MAX(p_likes) FROM posts WHERE date_month == ? AND class_group == 4)",
	 (today, today,))
	today_posts.append(db.fetchall())
	db.execute("SELECT id FROM posts WHERE date_month == ? AND class_group == 5 AND p_likes=(SELECT MAX(p_likes) FROM posts WHERE date_month == ? AND class_group == 5)",
	 (today, today,))
	today_posts.append(db.fetchall())
	db.execute("SELECT id FROM posts WHERE date_month == ? AND class_group == 6 AND p_likes=(SELECT MAX(p_likes) FROM posts WHERE date_month == ? AND class_group == 6)",
	 (today, today,))
	today_posts.append(db.fetchall())
	db.execute("SELECT id FROM posts WHERE date_month == ? AND class_group == 7 AND p_likes=(SELECT MAX(p_likes) FROM posts WHERE date_month == ? AND class_group == 7)",
	 (today, today,))
	today_posts.append(db.fetchall())
	db.execute("SELECT id FROM posts WHERE date_month == ? AND class_group == 8 AND p_likes=(SELECT MAX(p_likes) FROM posts WHERE date_month == ? AND class_group == 8)",
	 (today, today,))
	today_posts.append(db.fetchall())
	
	db.execute("SELECT user_id FROM users WHERE bot_cond == 3")

	for user in db.fetchall():
		db.execute("SELECT gid FROM Usersgroups WHERE uid == ?", (user,))

		for group in db.fetchall():
			if today_posts[int(group)-1]:
				db.execute("SELECT p_text FROM posts WHERE id == ?", (today_posts[int(group)-1][0],))
				ptext = db.fetchall()
				bot.send_message(user, "Evening QMUL for category: "+category_name.get(str(group))+"\n\n"+ptext[0], False)

			else:
				bot.send_message(user, "Sorry, no news today for category: "+category_name.get(str(group)), False)

				