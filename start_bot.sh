#!/bin/bash

# Скрипт для запуска Aviasales Telegram Bot

cd /home/ubuntu/TG_Aviasales

# Активация виртуального окружения
source venv/bin/activate

# Запуск бота
echo "🚀 Запуск Aviasales Telegram Bot..."
python telegram_bot.py 