#!/bin/bash

# Скрипт развертывания Aviasales Telegram Bot на Ubuntu 24.04
# Запускать с правами sudo

set -e

echo "🚀 Начинаем развертывание Aviasales Telegram Bot..."

# Обновление системы
echo "📦 Обновление системы..."
apt update && apt upgrade -y

# Установка Python и необходимых пакетов
echo "🐍 Установка Python и зависимостей..."
apt install -y python3 python3-pip python3-venv git curl

# Создание пользователя для бота (если не существует)
if ! id "ubuntu" &>/dev/null; then
    echo "👤 Создание пользователя ubuntu..."
    useradd -m -s /bin/bash ubuntu
fi

# Переход в домашнюю директорию пользователя
cd /home/ubuntu

# Клонирование или обновление репозитория
if [ -d "TG_Aviasales" ]; then
    echo "📁 Обновление существующего репозитория..."
    cd TG_Aviasales
    git pull
else
    echo "📁 Клонирование репозитория..."
    git clone https://github.com/yourusername/TG_Aviasales.git
    cd TG_Aviasales
fi

# Создание виртуального окружения
echo "🔧 Создание виртуального окружения..."
python3 -m venv venv
source venv/bin/activate

# Установка зависимостей
echo "📚 Установка Python зависимостей..."
pip install --upgrade pip
pip install -r requirements.txt

# Создание .env файла если не существует
if [ ! -f ".env" ]; then
    echo "⚙️ Создание файла конфигурации..."
    cp env_example .env
    echo "❗ ВАЖНО: Отредактируйте файл .env и добавьте ваши токены!"
    echo "   nano /home/ubuntu/TG_Aviasales/.env"
fi

# Установка прав доступа
echo "🔐 Настройка прав доступа..."
chown -R ubuntu:ubuntu /home/ubuntu/TG_Aviasales
chmod +x telegram_bot.py

# Копирование systemd service файла
echo "🔧 Настройка systemd сервиса..."
cp aviasales-bot.service /etc/systemd/system/
systemctl daemon-reload

# Включение автозапуска
echo "🔄 Включение автозапуска..."
systemctl enable aviasales-bot.service

echo "✅ Развертывание завершено!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Отредактируйте файл конфигурации:"
echo "   nano /home/ubuntu/TG_Aviasales/.env"
echo ""
echo "2. Запустите бота:"
echo "   systemctl start aviasales-bot"
echo ""
echo "3. Проверьте статус:"
echo "   systemctl status aviasales-bot"
echo ""
echo "4. Просмотр логов:"
echo "   journalctl -u aviasales-bot -f"
echo ""
echo "🎉 Бот готов к работе!" 