
# The CalDove Information Update System

from pickle import TRUE
from flask import Flask

from datetime import datetime, timedelta, timezone

from dateutil.relativedelta import relativedelta

import subprocess


app = Flask(__name__)

is_bot_running = False

def display_log(path):
    return open(path).read().replace("\n", "<br>")

@app.route('/bot_log')
def bot_log():
    site = "<h1>Telegram Bot Log</h1>"

    site += "<div id=\"log\">" + display_log("bot/botlog.txt") + "</div>"

    return site

@app.route('/access_log')
def access_log():
    site = "<h1>Telegram Access Log</h1>"

    site += "<div id=\"log\">" + display_log("bot/access_log.txt") + "</div>"

    return site

@app.route('/init')
def init():
    global is_bot_running
    subprocess.Popen(["python", "bot/bot.py"]) 
    site = "<h1>initiate Bot!</h1>"
    is_bot_running = True
    return site

@app.route('/')
def index():
    text = ""
    if is_bot_running:
        text+= "<h1>Bot is running...</h1>"
    else:
        text+= "<h1>Bot is offline.</h1>"
    text+= "<div id=\"content\"> <p>Links to Administration:</p><ul> <li><a href=\"init\">init Bot</a></li><li><a href=\"bot_log\">Bot Log</a></li><li><a href=\"access_log\">Access Log</a></li></ul></div>"
    return text


index()