#!/bin/bash
docker volume create mensabot_log
docker build ./ -t mensabot
docker run -p 5001:5000 -v mensabot_log:/app/log mensabot

