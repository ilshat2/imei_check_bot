from fastapi import FastAPI


app = FastAPI()

# Конфигурация
IMEI_CHECK_API_URL = 'https://imeicheck.net/api/check'
IMEI_CHECK_API_TOKEN = 'e4oEaZY1Kom5OXzybETkMlwjOCy3i8GSCGTHzWrhd4dc563b'
ALLOWED_TOKENS = ['api_token']  # Список допустимых токенов
