# MensaTelegramBridgeBot

MensaTelegramBridgeBot is a self-hostable Telegram-Bot that connects to the web interface of the "Mensa am Park" in Weimar and sends you every day all the vegan and vegetarian options available.
With a little bit of knowledge in Python the script can be easily adjusted for a different cafeteria.

## Installation
The bot ships with docker.
1. Get a telegram bot token and add them to the secrets config file.
2. Make sure docker is installed on your system, then run './install.sh' to get a running docker container.

If you don't want to use docker you can run the flask server directly after installing the requirements in the `requirements.txt`.
