import json
import requests

url = "https://www.cbr-xml-daily.ru/daily_json.js"
response = requests.get(url, timeout=10)

if response.status_code != 200:
    print(f"Ошибка запроса: {response.status_code}")
    exit()

data = response.json()


def get_rate(data, code):
    return data["Valute"][code]["Value"]


usd = get_rate(data, "USD")
eur = get_rate(data, "EUR")
cny = get_rate(data, "CNY")

print(f"Курс доллара: {usd:.2f} ₽")
print(f"Курс евро: {eur:.2f} ₽")
print(f"Курс юаня: {cny:.2f} ₽")

rates = {"USD": usd, "EUR": eur, "CNY": cny}

with open("rates.json", "w", encoding="utf-8") as f:
    json.dump(rates, f, ensure_ascii=False, indent=2)