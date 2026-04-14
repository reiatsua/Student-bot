# 🤖 Бот-помощник для учеников | Student Bot

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python&logoColor=white)
![Security](https://img.shields.io/badge/Security-Identity_Provider-red)

Клиентский Telegram-бот для учащихся Первого IT-лицея. Является неотъемлемой частью общей цифровой экосистемы лицея. Бот связывается с основным Django-порталом через API для синхронизации аккаунтов и получения актуального расписания.

## 🔗 Зависимости
Для полноценной работы функционала расписания и авторизации необходимо, чтобы был запущен **основной сайт лицея** (Django API).
* Репозиторий основного сайта: [First IT Lyceum](https://github.com/reiatsua/First_IT_Lyceum.git)

## 🛠 Технологии
* **Язык:** Python 3
* **Фреймворк:** `aiogram` 3.x (Асинхронный поллинг)
* **Сетевые запросы:** `requests`
* **Окружение:** `python-dotenv`

## 🚀 Как запустить локально

### 1. Подготовка
Склонируйте репозиторий на свой компьютер и перейдите в папку бота (для корректной работы назовите ее `student_bot`):
```bash
git clone https://github.com/reiatsua/Student-bot.git
cd student_bot
```

### 2. Виртуальное окружение
Создайте и активируйте виртуальное окружение:

Для Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

Для Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

Примечание: при ошибке выполнения на Windows попробуйте следующую команду:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Установка зависимостей
Установите необходимые библиотеки:
```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения
Создайте файл `.env` в корневой папке бота и добавьте следующие ключи:
```env
STUDENT_BOT_TOKEN=ваш_токен_бота_учеников_от_BotFather
DJANGO_API_URL=http://127.0.0.1:8000
```
*Убедитесь, что `DJANGO_API_URL` указывает на запущенный локальный сервер или реальный домен, иначе бот не сможет получать данные.*

### 5. Запуск
Запустите скрипт бота:
```bash
python student_bot.py
```
В консоли должно появиться сообщение об успешном запуске и ожидании команд.