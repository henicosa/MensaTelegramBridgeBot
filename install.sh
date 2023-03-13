#!/bin/bash
docker volume create mensabot_log
docker build ./ -t mensabot
docker run -p 5002:5000 -v mensabot_log:/app/log mensabot

