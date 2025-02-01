from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor
import requests


# Конфигурация
API_TOKEN = 'TELEGRAM_BOT_TOKEN'
IMEI_CHECK_API_URL = 'https://imeicheck.net/api/check'
IMEI_CHECK_API_TOKEN = 'e4oEaZY1Kom5OXzybETkMlwjOCy3i8GSCGTHzWrhd4dc563b'
WHITELIST = [123456789]  # Список разрешенных пользователей (Telegram ID)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


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


# Обработка IMEI
@dp.message_handler()
async def check_imei(message: types.Message):
    user_id = message.from_user.id
    if user_id not in WHITELIST:
        await message.reply("Доступ запрещен.")
        return

    imei = message.text.strip()
    if not is_valid_imei(imei):
        await message.reply("Некорректный IMEI. Пожалуйста, отправьте 15-значный номер.")
        return

    imei_info = get_imei_info(imei)
    await message.reply(f"Информация о IMEI:\n{imei_info}", parse_mode=ParseMode.MARKDOWN)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
