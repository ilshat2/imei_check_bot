from fastapi import FastAPI, HTTPException, Header
from typing import Dict
import requests
import uvicorn


app = FastAPI()


class Config:
    '''Конфигурационный класс для хранения API токенов и URL-ов.'''
    IMEI_CHECK_API_URL = 'https://imeicheck.net/api/check'
    IMEI_CHECK_API_TOKEN = 'e4oEaZY1Kom5OXzybETkMlwjOCy3i8GSCGTHzWrhd4dc563b'
    ALLOWED_TOKENS = {'api_token'}  # Множество допустимых токенов


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


@app.post('/api/check-imei')
async def check_imei(imei: str, token: str = Header(...)):
    '''Эндпоинт для проверки IMEI через API.'''
    if token not in Config.ALLOWED_TOKENS:
        raise HTTPException(status_code=403, detail='Доступ запрещен.')

    if not IMEIChecker.is_valid_imei(imei):
        raise HTTPException(status_code=400, detail='Некорректный IMEI.')

    imei_info = IMEIChecker.get_imei_info(imei)
    return imei_info


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
