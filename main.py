from aiogram import Bot, Dispatcher, types
import requests


# Конфигурация
API_TOKEN = 'TELEGRAM_BOT_TOKEN'
IMEI_CHECK_API_URL = 'https://imeicheck.net/api/check'
IMEI_CHECK_API_TOKEN = 'e4oEaZY1Kom5OXzybETkMlwjOCy3i8GSCGTHzWrhd4dc563b'
WHITELIST = [123456789]  # Список разрешенных пользователей (Telegram ID)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# Проверка валидности IMEI
def is_valid_imei(imei: str) -> bool:
    return imei.isdigit() and len(imei) == 15


# Запрос к API imeicheck.net
def get_imei_info(imei: str) -> dict:
    headers = {'Authorization': f'Bearer {IMEI_CHECK_API_TOKEN}'}
    response = requests.post(IMEI_CHECK_API_URL, json={'imei': imei}, headers=headers)
    return response.json()


# Обработка команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Отправь мне IMEI для проверки.")

