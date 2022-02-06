import sqlite3 as sl

from os.path import exists

## 
## Interface for bot 
##


class Database:

    def __init__(self):
        self.users = {}
        self.database = load_database()

    def has_user_subscribed_meal(self, user, meal):
        return meal in self.users[user]["subscribed_food"]

    def remove_subscription_from_user(self, user, meal):
        self.users[user]["subscribed_food"].remove(meal)

    def add_subscription_to_user(self, user, meal):
        self.users[user]["subscribed_food"] = self.users[user]["subscribed_food"].append(meal)

    def add_user_if_unknown(self, update):
        if update.message.chat.id not in self.users:
            self.users[update.message.chat.id] = {"first_name": update.message.from_user.first_name, \
                                                    "last_name": update.message.from_user.last_name, \
                                                    "username": update.message.from_user.username,   \
                                                    "chat_id": update.message.chat.id, \
                                                    "user_id": update.message.from_user.id, \
                                                    "subscribed_foods": []}



##
## Interne Methoden
##


def load_database():
    database_exists = exists('log/mensadaten.db')
    database = sl.connect('log/mensadaten.db')
    if not database_exists:
        init_database(database)
    return database

def init_database(database):
    print("[Database Handler] Database not found. Create new one...")
    database.execute("""
        CREATE TABLE USER (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            chatid TEXT
        );
    """)

def add_attribute_in_table(database, table, attribute, attribute_type):
    print("[Database Handler] Database not found. Create new one...")
    database.execute("""
        ALTER TABLE""" + table + """ADD COLUMN""" + attribute + " " + attribute_type + """;
    """)

def is_item_in_table(database, table, property, value):
    database.execute("SELECT EXISTS(SELECT 1 FROM " + table +" WHERE " + property + "=? LIMIT 1)", (value,))
    record = database.fetchone()
    if record[0] == 1:
        return True
    else:
        return False


def add_user(database, name, chatid):
    print(is_item_in_table("USER", "chatid", chatid))
    if not is_item_in_table("USER", "chatid", chatid):
        sql = 'INSERT INTO USER (name, chatid) values(?, ?)'
        database.execute(sql, (name, chatid))


def test(database):

    with database:

        database = database.cursor()
        add_user("ludwig", "4q30974107")
        add_user("52li", "3526225235102")

        data = database.execute("SELECT * FROM USER")
        for row in data:
            print(row)


database = load_database()
