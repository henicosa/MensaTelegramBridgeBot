from flask import Flask, Response, render_template, jsonify, request
from flask_basicauth import BasicAuth

import subprocess
import time
import json

def read_json(path):
    with open(path) as f:
        return json.load(f)

app = Flask(__name__)

with open('secrets/secrets.json') as f:
    secrets = json.load(f)

app.config['BASIC_AUTH_USERNAME'] = secrets['username']
app.config['BASIC_AUTH_PASSWORD'] = secrets['password']
basic_auth = BasicAuth(app)

program_status = "not running"

'''
-----------------------------------------------------

Section for App-specific functions

-----------------------------------------------------
'''

'''
-----------------------------------------------------

Section for template functions

-----------------------------------------------------
'''

# Main route

@app.route('/')
def index():
    return render_template('index.html', **read_json("application.json"))

@app.route('/status')
def status():
    global program_status
    return jsonify(status=program_status)

@app.route('/activate', methods=['POST'])
def activate():
    global program_status
    if program_status == "success":
        return jsonify(status='already running')
    program_running = True
    if start():
        program_status = "success"
    else:
        program_status = "failed"
    return jsonify(status=program_status)

def start():
    time.sleep(5)
    # code for your function goes here
    subprocess.Popen(["python", "bot/bot.py"]) 
    print("Bot started.")
    return True

# Logs

@app.route('/bot_log')
@basic_auth.required
def botlogs():
    log_messages = []
    with open('log/bot_log.txt', 'r') as logfile:
        for line in logfile:
            try:
                time, application, log_type, message = line.strip().split(' ', 3)
                log_messages.append({'time': time, 'application': application, 'type': log_type, 'message': message})
            except Exception as e:
                print("Parse Error for log event:" + line)
    log_messages = log_messages[::-1]  # Reverse the order of the messages to display the latest message first
    return render_template('logs.html', log_messages=log_messages)

def display_log(path):
    return open(path).read().replace("\n", "<br>")

@app.route('/access_log')
@basic_auth.required
def accesslogs():
    site = "<h1>Telegram Access Log</h1>"
    site += "<div id=\"log\">" + display_log("log/access_log.txt") + "</div>"
    return site


if __name__ == '__main__':
    app.run()