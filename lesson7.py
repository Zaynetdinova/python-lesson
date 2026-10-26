import os

import pandas as pd
import requests
from dotenv import load_dotenv

# --- Секреты из .env ---
load_dotenv()

token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

if token is None or chat_id is None:
    print("TELEGRAM_BOT_TOKEN или TELEGRAM_CHAT_ID не найден в .env")
    exit()


# --- Функция отправки ---
def send_message(text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        response = requests.post(url, json={"chat_id": chat_id, "text": text}, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        print("Не удалось отправить сообщение в Telegram (проверь токен и chat_id).")
        exit()


# --- Запрос курсов ---
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

# --- Таблица pandas ---
df = pd.DataFrame.from_dict(data["Valute"], orient="index")

df["rate"] = df["Value"] / df["Nominal"]
df["prev"] = df["Previous"] / df["Nominal"]
df["change_pct"] = ((df["rate"] - df["prev"]) / df["prev"] * 100).round(2)

selected = df[df["CharCode"].isin(["USD", "EUR", "CNY", "KZT", "TRY"])]
selected = selected.sort_values("change_pct", ascending=False)
print(selected[["CharCode", "rate", "change_pct"]])

# --- Текст сообщения ---
lines = ["Курсы валют ЦБ РФ:"]
for _, row in selected.iterrows():
    arrow = "▲" if row["change_pct"] > 0 else "▼" if row["change_pct"] < 0 else "="
    lines.append(f"{row['CharCode']}: {row['rate']:.2f} ₽ {arrow} {row['change_pct']:+.2f}%")

top = selected.loc[selected["change_pct"].abs().idxmax()]  # таблица отсортирована по change_pct по убыванию
lines.append("")
lines.append(f"Больше всего выросла: {top['CharCode']} ({top['change_pct']:+.2f}%)")

text = "\n".join(lines)
print(text)

# --- Отправка ---
send_message(text)
print("Сообщение отправлено")