import sqlite3


def db_bot():
    con = sqlite3.connect('bot_db.sqlite')
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS users (user_id VARCHAR NOT NULL, reg_date TEXT DEFAULT (null), bcond NUMERIC NOT NULL DEFAULT (0), user_name TEXT, first_name TEXT, last_name TEXT,   PRIMARY KEY(`id`))")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS Sources (id VARCHAR, name VARCHAR, s_link VARCHAR)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS Usersgroups (uid VARCHAR NOT NULL, gid VARCHAR NOT NULL)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS Reviews (uid VARCHAR NOT NULL, rev_text VARCHAR DEFAULT (null), rev_date TEXT)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS Posts (id VARCHAR PRIMARY KEY NOT NULL, gid VARCHAR NOT NULL, p_date VARCHAR NOT NULL DEFAULT (null), p_text VARCHAR, p_likes NUMERIC NOT NULL DEFAULT (0), p_reposts  NUMERIC NOT NULL DEFAULT (0), class_group VARCHAR)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS Categories (id VARCHAR, name VARCHAR)")
    con.commit()

db_bot()
