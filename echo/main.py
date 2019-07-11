import sqlite3

from telegram import Bot
from telegram import Update
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler

from echo.config import TG_TOKEN


def do_start(bot: Bot, update: Update):
    bot .send_message(
        chat_id=update.message.chat_id,
        text="puton",
    )


def db_bot():
    print (1)
    con = sqlite3.connect('bot_database.sqlite')
    cur = con.cursor ()
    cur.execute("""CREATE TABLE users
                  (user_id integer, artist text, release_date text,
                   publisher text, media_type text)
               """)
    con.commit()


def main():
    bot = Bot(
        token=TG_TOKEN,
    )
    updater = Updater(
        bot=bot,
    )

    start_handler = CommandHandler("start", do_start)

    updater.dispatcher.add_handler(start_handler)

    updater.start_polling()
    updater.idle()

    db_bot()

if __name__ == '__main__':
    main()