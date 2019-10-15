from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import joblib

from twitterscraper import query_tweets
from datetime import timedelta, datetime
import datetime as dt

import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot('')

category_name =  {'1':'Events','2':'Career','3':'Sport','4':'Science','5':'Politics','6':'Education','7':'Culture','8':'Freebies'}
bot_condition = {'1': 'New user', '2': 'News as post', '3': 'Evening QMUL'}

# get tweets from twitter 
def scrap_tweets():
    
    date_N_days_ago = datetime.now() - timedelta(days=1)
    y = int(date_N_days_ago.strftime("%Y"))
    m = int(date_N_days_ago.strftime("%m"))
    d = int(date_N_days_ago.strftime("%d"))

    # Import of classification model
    filename1 = 'model.sav'
    filename2 = 'tfidf.sav'
    model = joblib.load(filename1)
    tfidf = joblib.load(filename2)

    # Connection with database 
    database = sqlite3.connect('bot_db.sqlite')
    database.row_factory = lambda cursor, row: row[0]
    db = database.cursor()

    # Tweets from chosen 8 QMUL accounts will be returned
    for tweet in query_tweets("from%3AQMUL%20OR%20from%3AQMSU%20OR%20from%3Aqmcareers%20OR%20from%3AQMLibrary%20OR%20from%3AQMSU_Events%20OR%20from%3AEngageQM%20OR%20from%3AQMULSciEng%20OR%20from%3AQMSUsocieties", begindate=dt.date(y, m, d)):
        (category_name.get(str(model.predict(tfidf.transform([tweet.text])))))
        if tweet.tweet_id not in db.execute('SELECT id FROM Posts').fetchall():
            category = int((model.predict(tfidf.transform([tweet.text]))[0]))
            text = tweet.text.replace('http', ' http')
            text = text.replace('pic.', ' pic.')
            db.execute("INSERT INTO Posts (id, gid, p_date, p_text, p_likes, p_reposts, class_group, date_month) VALUES "
                   "(?, ?, ?, ?, ?, ?, ?, ?)",
                   (tweet.tweet_id, tweet.user_id, tweet.timestamp, text, tweet.likes, tweet.retweets,
                    category, datetime.now().strftime("%d")))
            send_as_scrap(text, category)
    database.commit()
    database.close()

# send tweets to users
def send_as_scrap(text, category):

	database = sqlite3.connect('bot_db.sqlite')
	database.row_factory = lambda cursor, row: row[0]
	db = database.cursor()

	db.execute("SELECT uid FROM Usersgroups WHERE gid == ?", (category,))
	for user in db.fetchall():
		bot.send_message(user, "Message from category: "+category_name.get(str(category))+"\n\n"+text, False)

