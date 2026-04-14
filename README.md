# 🎓 Student Bot | Модуль взаимодействия с учениками

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python&logoColor=white)
![Security](https://img.shields.io/badge/Security-Identity_Provider-red)

Фронтенд-клиент экосистемы Первого IT-лицея, предназначенный для автоматизации повседневных задач учащихся через Telegram. Бот интегрируется с основным Django-порталом для синхронизации профилей и предоставления актуальных данных.

## 🎯 Основные функции
* **Интерактивное расписание:** Мгновенное получение актуального графика уроков напрямую из базы данных лицея.

* **Identity Provider:** Связка Telegram-аккаунта с учетной записью на портале для персонализации данных.

* **Push-уведомления:** Получение важных оповещений от администрации лицея в режиме реального времени.

## 🔗 Место в экосистеме

Бот является активным потребителем API основного узла. Для работы всех функций необходим запущенный бэкенд:

* **Основной портал (Django 6):** [First IT Lyceum Portal](https://github.com/reiatsua/First_IT_Lyceum.git)

* **Production URL:** https://firstitlyceum-production.up.railway.app/

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
DJANGO_API_URL=ссылка_на_домашнюю_страницу_сайта
```
*Убедитесь, что `DJANGO_API_URL` указывает на запущенный локальный сервер или реальный домен, иначе бот не сможет получать данные.*

### 5. Запуск
Запустите скрипт бота:
```bash
python student_bot.py
```
В консоли должно появиться сообщение об успешном запуске и ожидании команд.