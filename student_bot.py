import asyncio
import os
import aiohttp # <-- Заменили requests на асинхронный aiohttp
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

load_dotenv()

# --- ЗАГРУЗКА НАСТРОЕК ---
TOKEN = os.getenv('STUDENT_BOT_TOKEN')
# Берем домен из переменных. Если запускаем локально, подставится 127.0.0.1
BASE_URL = os.getenv('DJANGO_BASE_URL', 'http://127.0.0.1:8000')

SYNC_API_URL = f"{BASE_URL}/auth/api/sync-telegram/"
SCHEDULE_API_URL = f"{BASE_URL}/auth/api/get-schedule/"
# -------------------------

bot = Bot(token=TOKEN)
dp = Dispatcher()

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📅 Расписание на завтра")]
    ],
    resize_keyboard=True, 
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

    # Отправляем асинхронный запрос на Django-сайт
    try:
        async with aiohttp.ClientSession() as session:
            # Используем data, как и было у тебя (если Django ждет request.POST)
            async with session.post(SYNC_API_URL, data={'sync_code': sync_code, 'chat_id': chat_id}) as response:
                if response.status == 200:
                    await message.answer("✅ Отлично! Твой аккаунт успешно привязан. Теперь ты будешь получать сюда уведомления.")
                elif response.status == 404:
                    await message.answer("❌ Неверный код. Проверь его в личном кабинете на сайте и попробуй еще раз.")
                else:
                    await message.answer("⚠️ Произошла ошибка на сервере. Попробуй позже.")
                    
    except Exception as e:
        print(f"Ошибка соединения: {e}")
        await message.answer("⚠️ Сайт лицея сейчас недоступен.")

@dp.message(Command('schedule'))
@dp.message(F.text == "📅 Расписание на завтра")
async def schedule_cmd(message: types.Message):
    chat_id = message.chat.id
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(SCHEDULE_API_URL, data={'chat_id': chat_id}) as response:
                
                # Если сайт вернул ответ, пробуем вытащить JSON
                if response.status == 200:
                    data = await response.json()
                    await message.answer(data['text'], parse_mode='HTML')
                else:
                    data = await response.json()
                    error_text = data.get('error', 'Неизвестная ошибка сервера.')
                    await message.answer(f"⚠️ {error_text}")
                    
    except Exception as e:
        print(f"Ошибка соединения: {e}")
        await message.answer("⚠️ Сайт лицея сейчас недоступен.")

async def main():
    print("Бот для учеников запущен...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())