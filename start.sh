#!/bin/bash

# Проверяем, установлен ли git
if ! command -v git &> /dev/null; then
    echo "Git не установлен. Устанавливаем git..."
    sudo apt install git -y
fi

# Обновляем репозиторий
echo "Обновляем репозиторий..."
git pull

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
