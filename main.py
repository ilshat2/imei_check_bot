from aiogram import Bot, Dispatcher
import requests

# Конфигурация
API_TOKEN = 'TELEGRAM_BOT_TOKEN'
IMEI_CHECK_API_URL = 'https://imeicheck.net/api/check'
IMEI_CHECK_API_TOKEN = 'e4oEaZY1Kom5OXzybETkMlwjOCy3i8GSCGTHzWrhd4dc563b'
WHITELIST = [123456789]  # Список разрешенных пользователей (Telegram ID)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# Запрос к API imeicheck.net
def get_imei_info(imei: str) -> dict:
    headers = {'Authorization': f'Bearer {IMEI_CHECK_API_TOKEN}'}
    response = requests.post(IMEI_CHECK_API_URL, json={'imei': imei}, headers=headers)
    return response.json()
