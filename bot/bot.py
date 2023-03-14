# import telegram library
# SOURCE: https://www.geeksforgeeks.org/create-a-telegram-bot-using-python/
"""
This will contain the API key we got from BotFather to specify in which bot we are adding functionalities to using our python code.
"""
from urllib import request
from telegram.ext.updater import Updater

"""
This will invoke every time a bot receives an update i.e. message or command and will send the user a message.
"""
from telegram.update import Update
"""
We will not use its functionality directly in our code but when we will be adding the dispatcher it is required (and it will work internally)
"""
from telegram.ext.callbackcontext import CallbackContext
"""
This Handler class is used to handle any command sent by the user to the bot, a command always starts with “/” i.e “/start”,”/help” etc.
"""
from telegram.ext.commandhandler import CommandHandler
from telegram.ext import CallbackQueryHandler
"""
This Handler class is used to handle any normal message sent by the user to the bot,
"""
from telegram.ext.messagehandler import MessageHandler
"""
This will filter normal text, commands, images, etc from a sent message.
"""
from telegram.ext.filters import Filters

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

import datetime
import logging
import time

import json

# import web crawler
from bs4 import BeautifulSoup
import requests


logging.basicConfig(filename="log/bot_log.txt",
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)



secrets = {}

def load_secrets():
    lines = open("bot/secrets", "r").readlines()
    for line in lines:
        if line[0] != "#":
            line = line.replace("\n","")
            pair = line.split(" = ")
            secrets[pair[0]] = pair[1]
    

def log_access(update, action):
    # access log
    access_log = open("log/access_log.txt", "a")
    current_time = time.localtime()
    access_log.write(time.strftime('%Y-%m-%d %H:%M:%S GMT', current_time) + " " + update.message.from_user.first_name + " queried bot with " + action + "\n")
    access_log.close()

######################################
#
#
#
# web requests methods
#
######################################

def get_meals():
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    meals = []
    if soup.findAll("div", class_="row px-3 mb-2 rowMeal"):
        for meal in soup.findAll("div", class_="row px-3 mb-2 rowMeal"):
            if "Vegetarisch" in str(meal) or "Vegan" in str(meal):
                text = ""
                reply_markup = generate_reply_markup(meal)
                text += get_price_for_students(meal) + "   " + does_it_include_dead_animals(meal) + "\n\n"
                text += get_meal_name(meal) # + " Bewerten: " + get_vote_link(meal) + "\n\n"
                meals.append({"text":text,"markup":reply_markup})
    return meals

def does_it_include_dead_animals(meal):
    meal = str(meal)
    if 'Vegane Speisen' in meal:
        return "🥗 Vegan! 🥗"
    elif "Vegetarische Speisen" in meal:
        return "🥗 Vegetarisch! 🥗"
    else:
        return "❌ Fleisch! ❌"

def get_meal_name(meal):
    return remove_styling(meal.find("div", class_="mealText").contents[0])

def remove_styling(word):
    return word.replace("\n", "").replace("\n", "").strip()

def get_price_for_students(meal):
    return "【" +  str(meal.find("div", class_="mealPreise").contents[0]).split(" ")[0] + " €】"

def get_vote_link(meal):
    return "https://www.stw-thueringen.de/" + meal.find("a", string="Gericht bewerten")["href"]

######################################
#
#
#
# telegram methods
#
######################################

def debug(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("😍", callback_data='1'),
            InlineKeyboardButton("😐", callback_data='2'),
            InlineKeyboardButton("😖", callback_data='3'),
        ],
        [InlineKeyboardButton("Abonnieren", callback_data='3')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    #query.edit_message_text(text=f"Selected option: {query.data}")

# generate Reply markup for a specific meal
def generate_reply_markup(meal):
    meal_id = get_meal_name(meal)
    vote_link = get_vote_link(meal)
    keyboard = [
            [
                InlineKeyboardButton("📝  Bewerten", url=vote_link),
                InlineKeyboardButton("🔔  Abonnieren", callback_data="2"),
            ],
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

# start conversation with the bot
def start(update: Update, context: CallbackContext):
    log_access(update, "start")
    #users[update.message.chat.id] = update.message.from_user
    db.add_user_if_unknown(update)
    update.message.reply_text("Mjamm... Ich bin dein Speiseplanbot und versorge dich täglich um 8 Uhr oder durch den Befehl /mensa mit dem heutigen Angebot in der Mensa am Park. Guten Appetit!")

def help(update: Update, context: CallbackContext):
    log_access(update, "help")
    update.message.reply_text("Es gibt eigentlich nicht viel über mich zu erzählen. Ich schicke dir täglich um 8 Uhr das Speisenangebot, wenn es etwas in der Mensa gibt.")

def backup(update: Update, context: CallbackContext):
    log_access(update, "backup")
    backup_dicts_to_json()
    update.message.reply_text("Backup fertig!")



def mensa(update: Update, context: CallbackContext):
    log_access(update, "mensa")
    meals = get_meals()
    if meals:
        update.message.reply_text("Hello, heute gibt es in der Mensa:")
    else:
        update.message.reply_text("Sorry 😓 die Mensa scheint heute nichts anzubieten...")
    for meal in meals:
        print(meal["text"] +"\n")
        print("send reply markup")
        #update.message.reply_text('Please choose:', reply_markup=reply_markup)

        update.message.reply_text(meal["text"], reply_markup=meal["markup"])

def dm(update: Update, context: CallbackContext):
    daily_menue(CallbackContext)

def daily_menue(context: CallbackContext):
    print("Send scheduled messages")    
    meals = get_meals()
    # send message to all users
    for chat_id in db.users.keys():
            if meals:
                print("Send scheduled message with menue")
                deliver_message_safely(bot, chat_id, "📣 Hello, heute gibt es in der Mensa:")
                for meal in meals:
                    deliver_markup_message_safely(bot, chat_id, meal["text"], meal["markup"])
            else:
                print("Send scheduled message without menue")
                deliver_message_safely(bot, chat_id, "📣 Sorry 😓 die Mensa scheint heute nichts für dich anzubieten...")
                
def deliver_message_safely(bot, chat_id, text):
    print("deliver message safely: " + text)
    message_delivered = False
    attempts = 0
    while not message_delivered and attempts < 1500:
        time.sleep(1)
        attempts+= 1
        print("with " + str(attempts) + " attempts")
        try:
            bot.send_message(chat_id=chat_id, text=text)
            message_delivered = True
        except Exception as e: 
            print(e)
            message_delivered = False

def deliver_markup_message_safely(bot, chat_id, text, markup):
    print("deliver message safely: " + text)
    message_delivered = False
    attempts = 0
    while not message_delivered and attempts < 15:
        time.sleep(1)
        attempts+= 1
        try:
            bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
            message_delivered = True
        except:
            message_delivered = False

    

def uptime_heartbeat(context: CallbackContext):
    print("send alive signal to uptime bot")
    requests.get(secrets["uptime_url"])

def scheduled_backup(context: CallbackContext):
    backup_dicts_to_json()

def backup_dicts_to_json():
    print("start backup")
    json_object = json.dumps(db.users, indent=4)
    print("json object created")
    with open("log/users.json", "w") as outfile:
        outfile.write(json_object)
        print("wrote it to file")

def restore_dicts_if_possible():
    if exists('log/users.json'):
        with open('log/users.json', 'r') as openfile:
            dict_object = json.load(openfile)
            db.users = dict_object
    
url = "https://www.stw-thueringen.de/mensen/weimar/mensa-am-park.html"
headers = {'user-agent': 'mensatelegrambridgebot_2022'}

if __name__ == "__main__":
    load_secrets()
    from database import *
    db = Database()
    restore_dicts_if_possible()
    
    updater = Updater(secrets["telegram_bot_token"],
                    use_context=True)
    job_daily_call = updater.job_queue.run_daily(daily_menue, days=(0, 1, 2, 3, 4, 5, 6), time=datetime.time(hour=7, minute=00, second=00))
    uptime_heartbeat_call = updater.job_queue.run_repeating(uptime_heartbeat, datetime.timedelta(minutes=3))
    backup_dicts_to_json_call = updater.job_queue.run_repeating(scheduled_backup, datetime.timedelta(hours=3))

    bot = updater.dispatcher.bot

    updater.dispatcher.add_handler(CommandHandler('mensa', mensa))
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('debug', debug))
    updater.dispatcher.add_handler(CommandHandler('dm', dm))
    updater.dispatcher.add_handler(CommandHandler('backup', backup))
    #job_daily = job_queue.run_daily(daily_suggestion, days=(0, 1, 2, 3, 4, 5, 6), time=datetime.time(hour=8, minute=00, second=00))

    updater.start_polling()
    updater.idle()

