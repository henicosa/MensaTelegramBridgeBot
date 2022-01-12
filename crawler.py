# import telegram library
# SOURCE: https://www.geeksforgeeks.org/create-a-telegram-bot-using-python/
"""
This will contain the API key we got from BotFather to specify in which bot we are adding functionalities to using our python code.
"""
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
"""
This Handler class is used to handle any normal message sent by the user to the bot,
"""
from telegram.ext.messagehandler import MessageHandler
"""
This will filter normal text, commands, images, etc from a sent message.
"""
from telegram.ext.filters import Filters

# import web crawler
from bs4 import BeautifulSoup
import requests

def get_meals():
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    text = ""
    for meal in soup.findAll("div", class_="row px-3 mb-2 rowMeal"):
        text += get_price_for_students(meal) + " " + get_meal_name(meal) + "\n"
        text += does_it_include_dead_animals(meal) + " Bewerten: " + get_vote_link(meal) + "\n\n"
    return text

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

# telegram methods
  
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Mjamm... Ich bin dein Speiseplanbot und versorge dich täglich um 8 Uhr oder durch den Befehl /mensa mit dem heutigen Angebot in der Mensa am Park. Guten Appetit!")

def help(update: Update, context: CallbackContext):
    update.message.reply_text("Es gibt eigentlich nicht viel über mich zu erzählen. Ich schicke dir täglich um 8 Uhr das Speisenangebot, wenn es etwas in der Mensa gibt.")

def mensa(update: Update, context: CallbackContext):
    update.message.reply_text(get_meals())

url = "https://www.stw-thueringen.de/mensen/weimar/mensa-am-park.html"
headers = {'user-agent': 'mensatelegrambridgebot_2022'}
telegram_bot_token = open("telegram_bot_token", "r").read().replace("\n","")
updater = Updater(telegram_bot_token,
                  use_context=True)

updater.dispatcher.add_handler(CommandHandler('mensa', mensa))
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.start_polling()
