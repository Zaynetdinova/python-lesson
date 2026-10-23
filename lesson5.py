import requests

import os
from dotenv import load_dotenv

load_dotenv()
if os.getenv("MY_API_KEY") is None:
    print("Ключ не найден в .env")

url = "https://www.cbr-xml-daily.ru/daily_json.js"

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.ConnectionError:
    print("Нет соединения с интернетом или сайт недоступен.")
    exit()
except requests.exceptions.Timeout:
    print("Сервер не ответил за 10 секунд.")
    exit()
except requests.exceptions.RequestException as e:
    print(f"Ошибка запроса: {e}")
    exit()


def get_rate(data, code):
    try:
        return data["Valute"][code]["Value"]
    except KeyError:
        print(f"Валюты {code} нет в ответе")
        return None


usd = get_rate(data, "USD")
eur = get_rate(data, "EUR")
cny = get_rate(data, "CNY")
xxx = get_rate(data, "XXX")    # проверка несуществующей валюты

if usd is not None: 
    print(f"Курс доллара: {usd:.2f} ₽")
if eur is not None: 
    print(f"Курс евро: {eur:.2f} ₽")
if cny is not None: 
    print(f"Курс юаня: {cny:.2f} ₽")
