#!/bin/bash

# Определяем директорию, где находится сам скрипт
SCRIPT_DIR=$(dirname "$(realpath "$BASH_SOURCE")")
cd "$SCRIPT_DIR"

# Проверяем, установлен ли git
if ! command -v git &> /dev/null; then
    echo "Git не установлен. Устанавливаем git..."
    sudo apt install git -y
fi

if [ ! -d ".git" ]; then
    echo "Клонируем репозиторий..."
    git clone https://github.com/Bainal/Telegram_PassBank.git temp
    mv temp/.git ./
    rm -rf temp
    git checkout .
else
    echo "Обновляем репозиторий..."
    git fetch --all
    git reset --hard HEAD
fi

# Проверяем, установлен ли python3-venv
if ! dpkg -s python3-venv > /dev/null 2>&1; then
    echo "Устанавливаем python3-venv..."
    sudo apt install python3-venv -y
fi

# Создаем виртуальное окружение (если не создано ранее)
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Активируем виртуальное окружение
source venv/bin/activate

# Устанавливаем зависимости
pip install -r requirements.txt

# Запускаем приложение
python main.py

# Пауза (если нужно)
read -p "Press Enter to continue..."

# Деактивируем виртуальное окружение
deactivate