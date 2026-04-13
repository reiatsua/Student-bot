import asyncio
import os
import requests
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

load_dotenv()

# --- ЗАГРУЗКА НАСТРОЕК ---
TOKEN = os.getenv('STUDENT_BOT_TOKEN')
BASE_URL = os.getenv('DJANGO_BASE_URL', 'http://127.0.0.1:8000') # Базовый адрес сайта

# Автоматически собираем полные пути к API
SYNC_API_URL = f"{BASE_URL}/auth/api/sync-telegram/"
SCHEDULE_API_URL = f"{BASE_URL}/auth/api/get-schedule/"
# -------------------------

bot = Bot(token=TOKEN)
dp = Dispatcher()

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📅 Расписание на завтра")]
    ],
    resize_keyboard=True, # Делает кнопку аккуратной
    input_field_placeholder="Выбери действие..."
    
)

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(
        "Привет! Я умный помощник Первого IT-лицея. 🤖\n\n"
        "Чтобы я мог присылать тебе расписание и важные уведомления, нам нужно связать аккаунты.\n"
        "Зайди в личный кабинет на сайте, нажми «Привязать Telegram» и отправь мне 6-значный код.",
        reply_markup=main_kb
    )

@dp.message(F.text.regexp(r'^\d{6}$'))
async def process_sync_code(message: types.Message):
    """Ловит сообщения, состоящие ровно из 6 цифр"""
    sync_code = message.text
    chat_id = message.chat.id

    # Отправляем запрос на Django-сайт для проверки кода
    try:
        response = requests.post(SYNC_API_URL, data={
            'sync_code': sync_code,
            'chat_id': chat_id
        })
        
        if response.status_code == 200:
            await message.answer("✅ Отлично! Твой аккаунт успешно привязан. Теперь ты будешь получать сюда уведомления.")
        elif response.status_code == 404:
            await message.answer("❌ Неверный код. Проверь его в личном кабинете на сайте и попробуй еще раз.")
        else:
            await message.answer("⚠️ Произошла ошибка на сервере. Попробуй позже.")
            
    except requests.exceptions.ConnectionError:
        await message.answer("⚠️ Сайт лицея сейчас недоступен. Запусти сервер Django!")

@dp.message(Command('schedule'))
@dp.message(F.text == "📅 Расписание на завтра")
async def schedule_cmd(message: types.Message):
    chat_id = message.chat.id
    
    # URL API в Django (позже заменить 127.0.0.1 на реальный домен сайта)
    url = 'http://127.0.0.1:8000/auth/api/get-schedule/'
    
    try:
        # Стучимся на сайт
        response = requests.post(SCHEDULE_API_URL, data={'chat_id': chat_id})
        data = response.json()
        
        if response.status_code == 200:
            # Сайт всё нашел и прислал готовый текст
            await message.answer(data['text'], parse_mode='HTML')
        else:
            # Сайт прислал ошибку (нет файла, нет привязки и т.д.)
            error_text = data.get('error', 'Неизвестная ошибка сервера.')
            await message.answer(f"⚠️ {error_text}")
            
    except requests.exceptions.ConnectionError:
        await message.answer("⚠️ Сайт лицея сейчас недоступен. Запусти сервер Django!")

async def main():
    print("Бот для учеников запущен...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())