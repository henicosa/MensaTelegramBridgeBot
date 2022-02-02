import sqlite3 as sl

from os.path import exists

def init_database():
    print("[Database Handler] Database not found. Create new one...")
    database.execute("""
        CREATE TABLE USER (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            chatid TEXT
        );
    """)


def is_item_in_table(table, property, value):
    database.execute("SELECT EXISTS(SELECT 1 FROM " + table +" WHERE " + property + "=? LIMIT 1)", (value,))
    record = database.fetchone()
    if record[0] == 1:
        return True
    else:
        return False


def add_user(name, chatid):
    print(is_item_in_table("USER", "chatid", chatid))
    if not is_item_in_table("USER", "chatid", chatid):
        sql = 'INSERT INTO USER (name, chatid) values(?, ?)'
        database.execute(sql, (name, chatid))


databse_exists = exists('log/mensadaten.db')
database = sl.connect('log/mensadaten.db')
if not databse_exists:
    init_database()

with database:

    database = database.cursor()
    add_user("ludwig", "4q30974107")
    add_user("52li", "3526225235102")

    data = database.execute("SELECT * FROM USER")
    for row in data:
        print(row)


