from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.dispatcher.filters import Command
from typing import Dict
import requests


class Config:
    '''Конфигурационный класс для хранения API токенов и URL-ов.'''
    API_TOKEN = 'TELEGRAM_BOT_TOKEN'
    IMEI_CHECK_API_URL = 'https://imeicheck.net/api/check'
    IMEI_CHECK_API_TOKEN = 'e4oEaZY1Kom5OXzybETkMlwjOCy3i8GSCGTHzWrhd4dc563b'
    WHITELIST = {123456789}  # Множество разрешенных пользователей (Telegram ID)


class IMEIChecker:
    '''Класс для работы с API проверки IMEI.'''
    @staticmethod
    def is_valid_imei(imei: str) -> bool:
        '''Проверяет, является ли IMEI корректным.'''
        return imei.isdigit() and len(imei) == 15

    @staticmethod
    def get_imei_info(imei: str) -> Dict:
        '''Запрашивает информацию об IMEI у внешнего API.'''
        headers = {'Authorization': f'Bearer {Config.IMEI_CHECK_API_TOKEN}'}
        response = requests.post(
            Config.IMEI_CHECK_API_URL,
            json={'imei': imei},
            headers=headers
        )
        return response.json() if response.status_code == 200 else {'error': 'Failed to fetch data'}


class TelegramBot:
    '''Основной класс Telegram-бота для проверки IMEI.'''
    def __init__(self):
        self.bot = Bot(token=Config.API_TOKEN)
        self.dp = Dispatcher(self.bot)
        self.dp.middleware.setup(LoggingMiddleware())
        self.register_handlers()

    def register_handlers(self):
        '''Регистрирует обработчики команд и сообщений.'''
        self.dp.register_message_handler(self.send_welcome, Command('start'))
        self.dp.register_message_handler(self.check_imei)

    async def send_welcome(self, message: types.Message):
        '''Отправляет приветственное сообщение пользователю.'''
        await message.reply('Привет! Отправь мне IMEI для проверки.')

    async def check_imei(self, message: types.Message):
        '''Обрабатывает сообщение с IMEI, проверяет и отправляет ответ пользователю.'''
        user_id = message.from_user.id
        if user_id not in Config.WHITELIST:
            await message.reply('Доступ запрещен.')
            return

        imei = message.text.strip()
        if not IMEIChecker.is_valid_imei(imei):
            await message.reply('Некорректный IMEI. Пожалуйста, отправьте 15-значный номер.')
            return

        imei_info = IMEIChecker.get_imei_info(imei)
        response_text = f'Информация о IMEI:\n{imei_info}' if 'error' not in imei_info else 'Ошибка при запросе к API.'

        await message.reply(response_text, parse_mode=ParseMode.MARKDOWN)

    def run(self):
        '''Запускает бота в режиме polling.'''
        executor.start_polling(self.dp, skip_updates=True)


if __name__ == '__main__':
    bot = TelegramBot()
    bot.run()
