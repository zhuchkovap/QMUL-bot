import telebot
from telebot import types
import sqlite3

import evening
import scrap
import time


bot = telebot.TeleBot('')

category_name =  {'1':'Events','2':'Career','3':'Sport','4':'Science','5':'Politics','6':'Education','7':'Culture','8':'Freebies'}
bot_condition = {'1': 'New user', '2': 'News as post', '3': 'Evening QMUL'}

# command start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    
    database = sqlite3.connect('bot_db.sqlite')
    db = database.cursor()

    db.execute("SELECT user_id FROM users WHERE user_id = ?", (message.chat.id,))
    check_user = db.fetchall()

    if not check_user:
        db.execute("INSERT INTO users (user_id, reg_date, bot_cond, user_name, first_name, last_name) VALUES "
                   "(?, datetime('now', 'localtime'), 1, ?, ?, ?)",
                   (message.chat.id, message.chat.username, message.chat.first_name, message.chat.last_name,))
        database.commit()

        bot.send_message(
            message.chat.id,
            "Hi, I'm a bot! \n"
                 "I'll help you to monitor news about your University! \U0001F609\n"
                 "I can send you posts from QMUL Twitter. \n"
                 "I also have an evening newsletter of popular news. \n\n\n"
                 "Please choose the type of the subscription. \n"
                 "Evening QMUL is an evening newsletter with the most popular news from each category. It is sent everyday at 9 p.m.\n"
                 "Or I can send you news as they post.\n",
            reply_markup=start_keyboard())
    else:
        bot.send_message(message.chat.id, 'Welcome to the main menu!', reply_markup=menu_keyboard()) 

# command stop
@bot.message_handler(commands=['stop'])
def send_goodbye(message):

    database = sqlite3.connect('bot_db.sqlite')
    db = database.cursor()

    db.execute("SELECT user_id FROM users WHERE user_id = ?", (message.chat.id,))
    check_user = db.fetchall()

    if check_user:
        db.execute("DELETE FROM users WHERE user_id = ?", (message.chat.id,))
        database.commit()
        db.execute("DELETE FROM Usersgroups WHERE uid = ?", (message.chat.id,))
        database.commit()

        bot.send_message(
            message.chat.id, 
            "Very sorry that you decided to unsubscribe from all QMUL news. \U0001F614\n"
            "If you want to join QMUL_bot again, press /start \U0001F609", False)

    else: 
        bot.send_message(message.chat.id, 'Please press /start to join the channel', False)

# command help
@bot.message_handler(commands=['help'])  
def send_help(message):   
    bot.send_message(  
        message.chat.id,  
        'To stop the bot from sending messages press /stop.\n' +  
        'To change your categories and subscription type press "manage subscriptions".\n',  
        reply_markup=menu_keyboard()  
    )

@bot.message_handler(content_types=["text"])
def main_menu(message):
    database = sqlite3.connect('bot_db.sqlite')
    database.row_factory = lambda cursor, row: row[0]
    db = database.cursor()
#1 screen with subscription types
    if message.text == 'Evening QMUL':
        db.execute("UPDATE users SET bot_cond = 3 WHERE user_id = ?", (message.chat.id,))
        database.commit()
        text = 'Great! You are subscribed to Evening QMUL. \n Please choose categories you are interested in: '
        bot.send_message(message.chat.id, text,reply_markup=cat_keyboard())

    if message.text == 'News as they post':
        db.execute("UPDATE users SET bot_cond = 2 WHERE user_id = ?", (message.chat.id,))
        database.commit()
        text = 'Great! You are subscribed to QMUL news as they post. \n Please choose categories you are interested in: '
        bot.send_message(message.chat.id, text,reply_markup=cat_keyboard())

#2 screen with categories
    if message.text == 'Events':
        db.execute("SELECT uid FROM Usersgroups WHERE uid = ? AND gid ==1", (message.chat.id,))
        check_user = db.fetchall()
        if not check_user:
            db.execute("INSERT INTO Usersgroups (uid, gid) VALUES "
                   "(?, 1)",
                   (message.chat.id,))
            database.commit()
            bot.send_message(message.chat.id, 'You added Events to your categories', False)
        else:
        	bot.send_message(message.chat.id, 'You already subscribed to Events', False)

    if message.text == 'Career':
        db.execute("SELECT uid FROM Usersgroups WHERE uid = ? AND gid ==2", (message.chat.id,))
        check_user = db.fetchall()
        if not check_user:
            db.execute("INSERT INTO Usersgroups (uid, gid) VALUES "
                   "(?, 2)",
                   (message.chat.id,))
            database.commit()
            bot.send_message(message.chat.id, 'You added Career to your categories', False)
        else:
        	bot.send_message(message.chat.id, 'You already subscribed to Career', False)

    if message.text == 'Sport':
        db.execute("SELECT uid FROM Usersgroups WHERE uid = ? AND gid ==3", (message.chat.id,))
        check_user = db.fetchall()
        if not check_user:
            db.execute("INSERT INTO Usersgroups (uid, gid) VALUES "
                   "(?, 3)",
                   (message.chat.id,))
            database.commit()
            bot.send_message(message.chat.id, 'You added Sport to your categories', False)
        else:
        	bot.send_message(message.chat.id, 'You already subscribed to Sport', False)

    if message.text == 'Science':
        db.execute("SELECT uid FROM Usersgroups WHERE uid = ? AND gid ==4", (message.chat.id,))
        check_user = db.fetchall()
        if not check_user:
            db.execute("INSERT INTO Usersgroups (uid, gid) VALUES "
                   "(?, 4)",
                   (message.chat.id,))
            database.commit()
            bot.send_message(message.chat.id, 'You added Science to your categories', False)
        else:
        	bot.send_message(message.chat.id, 'You already subscribed to Science', False)

    if message.text == 'Politics':
        db.execute("SELECT uid FROM Usersgroups WHERE uid = ? AND gid ==5", (message.chat.id,))
        check_user = db.fetchall()
        if not check_user:
            db.execute("INSERT INTO Usersgroups (uid, gid) VALUES "
                   "(?, 5)",
                   (message.chat.id,))
            database.commit()
            bot.send_message(message.chat.id, 'You added Politics to your categories', False)
        else:
        	bot.send_message(message.chat.id, 'You already subscribed to Politics', False)
    
    if message.text == 'Education':
        db.execute("SELECT uid FROM Usersgroups WHERE uid = ? AND gid ==6", (message.chat.id,))
        check_user = db.fetchall()
        if not check_user:
            db.execute("INSERT INTO Usersgroups (uid, gid) VALUES "
                   "(?, 6)",
                   (message.chat.id,))
            database.commit()
            bot.send_message(message.chat.id, 'You added Education to your categories', False)
        else:
        	bot.send_message(message.chat.id, 'You already subscribed to Education', False)

    if message.text == 'Culture':
        db.execute("SELECT uid FROM Usersgroups WHERE uid = ? AND gid ==7", (message.chat.id,))
        check_user = db.fetchall()
        if not check_user:
            db.execute("INSERT INTO Usersgroups (uid, gid) VALUES "
                   "(?, 7)",
                   (message.chat.id,))
            database.commit()
            bot.send_message(message.chat.id, 'You added Culture to your categories', False)
        else:
        	bot.send_message(message.chat.id, 'You already subscribed to Culture', False)

    if message.text == 'Freebies':
        db.execute("SELECT uid FROM Usersgroups WHERE uid = ? AND gid ==8", (message.chat.id,))
        check_user = db.fetchall()
        if not check_user:
            db.execute("INSERT INTO Usersgroups (uid, gid) VALUES "
                   "(?, 8)",
                   (message.chat.id,))
            database.commit()
            bot.send_message(message.chat.id, 'You added Freebies to your categories', False)
        else:
        	bot.send_message(message.chat.id, 'You already subscribed to Freebies', False)
       

    if message.text == 'Back to main menu':
        bot.send_message(message.chat.id, 'Welcome to the main menu!', reply_markup=menu_keyboard())

#4 screen with main menu    
    if message.text == 'About the project':
        bot.send_message(message.chat.id, 'QMUL_bot is the final project of QMUL EECS MSc student Polina Zhuchkova.\n'
                                      'It is the first news bot of Queen Mary University of London!\n'
                                      'Plagiarism and copying are prosecuted.', reply_markup=menu_keyboard())
        

#7 screen to manage subscriptions
    if message.text == 'Manage subscriptions':
        bot.send_message(message.chat.id, 'Please, choose what you want to do', reply_markup=manage_keyboard())   

    if message.text == 'My subscription':
        db.execute("SELECT bot_cond FROM users WHERE user_id = ?", (message.chat.id,))
        subtype = db.fetchall()[0]
        bot.send_message(message.chat.id, 'Your type of subscription is: '+bot_condition.get(str(subtype)))

        db.execute("SELECT gid FROM Usersgroups WHERE uid = ?", (message.chat.id,))
        categories_id = db.fetchall()
        categories = []

        if categories_id:
            for category in categories_id:
                categories.append(category_name.get(category))

            bot.send_message(message.chat.id, 'You are subscribed to : '+str(categories)+ " categories", reply_markup=manage_keyboard())
        else:
            bot.send_message(message.chat.id, 'You are not subscribed to any category', reply_markup=manage_keyboard())

    if message.text == 'Change subscription type':
        db.execute("SELECT bot_cond FROM users WHERE user_id = ?", (message.chat.id,))
        subtype = db.fetchall()[0]
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        
        if subtype==3:
        	markup.add(types.KeyboardButton('Change to News as post'))
        if subtype==2:
        	markup.add(types.KeyboardButton('Change to Evening QMUL'))
        markup.add(types.KeyboardButton('Back to main menu'))

        bot.send_message(message.chat.id, 'Your type of subscription is: '+bot_condition.get(str(subtype)) + "\n\nI have 2 types of subscription.\nEvening QMUL is an evening newsletter with the most popular news from your categories, it is sent everyday at 9 p.m.\nOr I can send you news as they post during the day.", reply_markup=markup)

    if message.text == 'Change to News as post':

        db.execute("UPDATE users SET bot_cond = 2 WHERE user_id = ?", (message.chat.id,))
        database.commit()

        bot.send_message(message.chat.id, 'Your type of subscription changed to News as post', reply_markup=menu_keyboard())

    if message.text == 'Change to Evening QMUL':

        db.execute("UPDATE users SET bot_cond = 3 WHERE user_id = ?", (message.chat.id,))
        database.commit()

        bot.send_message(message.chat.id, 'Your type of subscription changed to Evening QMUL', reply_markup=menu_keyboard())

    if message.text == 'Change categories':
        db.execute("SELECT gid FROM Usersgroups WHERE uid = ?", (message.chat.id,))
        categories_id = db.fetchall()
        categories = []

        if categories_id:
            for category in categories_id:
                categories.append(category_name.get(category))
            bot.send_message(message.chat.id, 'You are already subscribed to : \n'+str(categories), None)
        else:
        	bot.send_message(message.chat.id, 'You are not subscribed to any category', None)


        bot.send_message(message.chat.id, 'Choose what you want to do: ', reply_markup=mancat_keyboard())


    # 11 screen choose categories to subscribe 
    if message.text == 'Choose categories to subscribe':
        db.execute("SELECT gid FROM Usersgroups WHERE uid = ?", (message.chat.id,))
        categories_id = db.fetchall()

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        check_if_all = 0
        for category in category_name:
            if category not in categories_id:
                markup.add(types.KeyboardButton(category_name.get(str(category[0]))))
                check_if_all += 1

        markup.add(types.KeyboardButton('Back to main menu'))
        
        if check_if_all > 0:
            bot.send_message(message.chat.id, 'Please, select topics to add to your subscription.\n', reply_markup=markup)
            bot.send_message(message.chat.id, 'You are not subscribed to:', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'You are subscribed to all categories', reply_markup=manage_keyboard()) 

    # 11 screen choose categories to unsubscribe 
    if message.text == 'Unsubscribe from category':
        db.execute("SELECT gid FROM Usersgroups WHERE uid = ?", (message.chat.id,))
        categories_id = db.fetchall()

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        check_if_all = 0
        for category in category_name:
            if category in categories_id:
                markup.add(types.KeyboardButton("No more "+category_name.get(str(category[0]))))
                check_if_all += 1
        
        markup.add(types.KeyboardButton('Back to main menu'))

        if check_if_all > 0:
            bot.send_message(message.chat.id, 'Choose topics to unsubscribe: ', reply_markup=markup)

        else:
            bot.send_message(message.chat.id, 'You have no subscriptions yet', reply_markup=mancat_keyboard())

    #2 categories
    if message.text == 'No more Events':
        db.execute("SELECT uid FROM Usersgroups WHERE uid = ? AND gid ==1", (message.chat.id,))
        check_user = db.fetchall()
        if check_user:
            db.execute("DELETE FROM Usersgroups WHERE uid = ? AND gid ==1", (message.chat.id,))
            database.commit()
            bot.send_message(message.chat.id, 'You have unsubscribed from Events category', False)
        else:
        	bot.send_message(message.chat.id, 'You already unsubscribed from Events', False)

    if message.text == 'No more Career':
        db.execute("SELECT uid FROM Usersgroups WHERE uid = ? AND gid ==2", (message.chat.id,))
        check_user = db.fetchall()
        if check_user:
            db.execute("DELETE FROM Usersgroups WHERE uid = ? AND gid ==2", (message.chat.id,))
            database.commit()
            bot.send_message(message.chat.id, 'You have unsubscribed from Career category', False)
        else:
        	bot.send_message(message.chat.id, 'You already unsubscribed from Career', False)

    if message.text == 'No more Sport':
        db.execute("SELECT uid FROM Usersgroups WHERE uid = ? AND gid ==3", (message.chat.id,))
        check_user = db.fetchall()
        if check_user:
            db.execute("DELETE FROM Usersgroups WHERE uid = ? AND gid ==3", (message.chat.id,))
            database.commit()
            bot.send_message(message.chat.id, 'You have unsubscribed from Sport category', False)
        else:
        	bot.send_message(message.chat.id, 'You already unsubscribed from Sport', False)

    if message.text == 'No more Science':
        db.execute("SELECT uid FROM Usersgroups WHERE uid = ? AND gid ==4", (message.chat.id,))
        check_user = db.fetchall()
        if check_user:
            db.execute("DELETE FROM Usersgroups WHERE uid = ? AND gid ==4", (message.chat.id,))
            database.commit()
            bot.send_message(message.chat.id, 'You have unsubscribed from Science category', False)
        else:
        	bot.send_message(message.chat.id, 'You already unsubscribed from Science', False)

    if message.text == 'No more Politics':
        db.execute("SELECT uid FROM Usersgroups WHERE uid = ? AND gid ==5", (message.chat.id,))
        check_user = db.fetchall()
        if check_user:
            db.execute("DELETE FROM Usersgroups WHERE uid = ? AND gid ==5", (message.chat.id,))
            database.commit()
            bot.send_message(message.chat.id, 'You have unsubscribed from Politics category', False)
        else:
        	bot.send_message(message.chat.id, 'You already unsubscribed from Politics', False)
    
    if message.text == 'No more Education':
        db.execute("SELECT uid FROM Usersgroups WHERE uid = ? AND gid ==6", (message.chat.id,))
        check_user = db.fetchall()
        if check_user:
            db.execute("DELETE FROM Usersgroups WHERE uid = ? AND gid ==6", (message.chat.id,))
            database.commit()
            bot.send_message(message.chat.id, 'You have unsubscribed from Education category', False)
        else:
        	bot.send_message(message.chat.id, 'You already unsubscribed from Education', False)

    if message.text == 'No more Culture':
        db.execute("SELECT uid FROM Usersgroups WHERE uid = ? AND gid ==7", (message.chat.id,))
        check_user = db.fetchall()
        if check_user:
            db.execute("DELETE FROM Usersgroups WHERE uid = ? AND gid ==7", (message.chat.id,))
            database.commit()
            bot.send_message(message.chat.id, 'You have unsubscribed from Culture category', False)
        else:
        	bot.send_message(message.chat.id, 'You already unsubscribed from Culture', False)

    if message.text == 'No more Freebies':
        db.execute("SELECT uid FROM Usersgroups WHERE uid = ? AND gid ==8", (message.chat.id,))
        check_user = db.fetchall()
        if check_user:
            db.execute("DELETE FROM Usersgroups WHERE uid = ? AND gid ==8", (message.chat.id,))
            database.commit()
            bot.send_message(message.chat.id, 'You have unsubscribed from Freebies category', False)
        else:
        	bot.send_message(message.chat.id, 'You already unsubscribed from Freebies', False)
       

    database.close()   

# main menu keyboard
def menu_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(types.KeyboardButton('My subscription'))
    markup.add(types.KeyboardButton('Manage subscriptions'))
    markup.add(types.KeyboardButton('About the project'))

    return markup  

# welcome scr keyboard
def start_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    evnews_btn = types.KeyboardButton('Evening QMUL')
    dnews_btn = types.KeyboardButton('News as they post')
    markup.add(evnews_btn)
    markup.add(dnews_btn)
    return markup  

# buttons as categories 
def cat_keyboard():

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in categories_list():
        markup.add(types.KeyboardButton(i[0]))
    markup.add(types.KeyboardButton('Back to main menu'))
    return markup

# manage categories keyboard
def mancat_keyboard():

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(types.KeyboardButton('Unsubscribe from category'))
    markup.add(types.KeyboardButton('Choose categories to subscribe'))
    markup.add(types.KeyboardButton('Back to main menu'))

    return markup 

# manage keyboard
def manage_keyboard():

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Change subscription type'))
    markup.add(types.KeyboardButton('Change categories'))
    markup.add(types.KeyboardButton('Back to main menu'))
    return markup


def categories_list():

    database = sqlite3.connect('bot_db.sqlite')
    db = database.cursor()

    db.execute("SELECT name FROM Categories")
    categories = db.fetchall()

    database.close()
    return categories

def main():
    bot.remove_webhook()
    #bot.polling(none_stop=True)
    scrap.scrap_tweets()

if __name__ == "__main__":

    main()




