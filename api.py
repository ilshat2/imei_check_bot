from fastapi import FastAPI, HTTPException, Header
import requests
import uvicorn


app = FastAPI()

# Конфигурация
IMEI_CHECK_API_URL = 'https://imeicheck.net/api/check'
IMEI_CHECK_API_TOKEN = 'e4oEaZY1Kom5OXzybETkMlwjOCy3i8GSCGTHzWrhd4dc563b'
ALLOWED_TOKENS = ['api_token']  # Список допустимых токенов


# Проверка валидности IMEI
def is_valid_imei(imei: str) -> bool:
    return imei.isdigit() and len(imei) == 15


# Запрос к API imeicheck.net
def get_imei_info(imei: str) -> dict:
    headers = {'Authorization': f'Bearer {IMEI_CHECK_API_TOKEN}'}
    response = requests.post(IMEI_CHECK_API_URL, json={'imei': imei}, headers=headers)
    return response.json()


# Эндпоинт для проверки IMEI
@app.post("/api/check-imei")
async def check_imei(imei: str, token: str = Header(...)):
    if token not in ALLOWED_TOKENS:
        raise HTTPException(status_code=403, detail="Доступ запрещен.")

    if not is_valid_imei(imei):
        raise HTTPException(status_code=400, detail="Некорректный IMEI.")

    imei_info = get_imei_info(imei)
    return imei_info


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
