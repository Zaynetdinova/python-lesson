# Урок 8б: сводка курсов валют + комментарий Claude, отправка в Telegram
#
# Что делает скрипт:
# 1. Берёт курсы валют из API ЦБ РФ
# 2. Считает в pandas изменение курса за день
# 3. Просит Claude написать короткий комментарий к сводке
# 4. Отправляет сводку и комментарий в Telegram
#
# Нужные переменные в .env:
#   TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, ANTHROPIC_API_KEY

import os

import anthropic
import pandas as pd
import requests
from dotenv import load_dotenv

# --- 1. Секреты из .env ---
# load_dotenv() читает файл .env и кладёт значения в переменные окружения
load_dotenv()

token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")
anthropic_key = os.getenv("ANTHROPIC_API_KEY")

# Если хотя бы одного значения нет, дальше идти нет смысла
if token is None or chat_id is None or anthropic_key is None:
    print("Проверь .env: нужны TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID и ANTHROPIC_API_KEY")
    exit()

# Клиент Claude сам берёт ключ из переменной ANTHROPIC_API_KEY
client = anthropic.Anthropic()


# --- 2. Функция отправки в Telegram ---
def send_message(text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        response = requests.post(url, json={"chat_id": chat_id, "text": text}, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        # Саму ошибку не печатаем: в её тексте есть адрес с токеном
        print("Не удалось отправить сообщение в Telegram (проверь токен и chat_id).")
        exit()


# --- 3. Функция запроса к Claude ---
def ask_claude(prompt, system=None, max_tokens=500):
    """Отправляет запрос Claude. Возвращает текст ответа или None при ошибке."""
    params = {
        "model": "claude-haiku-5-5",
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }
    # system передаём только если он задан
    if system is not None:
        params["system"] = system

    try:
        message = client.messages.create(**params)
    except anthropic.AuthenticationError:
        print("Неверный ключ API (проверь ANTHROPIC_API_KEY в .env).")
        return None
    except anthropic.RateLimitError:
        print("Слишком много запросов, попробуй позже.")
        return None
    except anthropic.APIConnectionError:
        print("Нет соединения с API Claude.")
        return None
    except anthropic.APIStatusError as e:
        print(f"Ошибка API Claude, код {e.status_code}")
        return None

    if message.stop_reason == "max_tokens":
        print("Внимание: ответ Claude обрезан, увеличь max_tokens.")

    # Ответ состоит из блоков разных типов, берём только текстовые
    texts = [block.text for block in message.content if block.type == "text"]

    if not texts:
        print("В ответе Claude нет текста.")
        return None

    return "".join(texts)


# --- 4. Курсы валют из API ЦБ РФ ---
url = "https://www.cbr-xml-daily.ru/daily_json.js"

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.ConnectionError:
    print("Нет соединения с интернетом или сайт ЦБ недоступен.")
    exit()
except requests.exceptions.Timeout:
    print("Сервер ЦБ не ответил за 10 секунд.")
    exit()
except requests.exceptions.RequestException as e:
    print(f"Ошибка запроса к ЦБ: {e}")
    exit()

# --- 5. Таблица pandas и расчёт изменения ---
# Словарь «код валюты -> данные» превращаем в таблицу, где каждая валюта это строка
df = pd.DataFrame.from_dict(data["Valute"], orient="index")

# Делим на Nominal: у некоторых валют курс указан за 10 или 100 единиц
df["rate"] = df["Value"] / df["Nominal"]
df["prev"] = df["Previous"] / df["Nominal"]

# Изменение за день в процентах: (новое - старое) / старое * 100
df["change_pct"] = ((df["rate"] - df["prev"]) / df["prev"] * 100).round(2)

# Оставляем нужные валюты и сортируем: сверху те, что выросли сильнее всего
selected = df[df["CharCode"].isin(["USD", "EUR", "CNY", "KZT", "TRY"])]
selected = selected.sort_values("change_pct", ascending=False)

if selected.empty:
    print("В ответе ЦБ не нашлось нужных валют.")
    exit()

# --- 6. Текст сводки ---
lines = ["Курсы валют ЦБ РФ:"]
for _, row in selected.iterrows():
    arrow = "▲" if row["change_pct"] > 0 else "▼" if row["change_pct"] < 0 else "="
    lines.append(f"{row['CharCode']}: {row['rate']:.2f} ₽ {arrow} {row['change_pct']:+.2f}%")

# Первая строка таблицы после сортировки: у неё самое большое изменение
top = selected.loc[selected["change_pct"].abs().idxmax()]
lines.append("")
lines.append(f"Больше всего изменилась: {top['CharCode']} ({top['change_pct']:+.2f}%)")

text = "\n".join(lines)
print(text)

# --- 7. Комментарий Claude ---
# Длину задаём в самом запросе, а max_tokens оставляем с запасом
comment = ask_claude(
    f"Вот сводка курсов валют за день:\n{text}\n\n"
    "Напиши комментарий в 2-3 предложениях: что изменилось и на что обратить внимание.",
    system="Ты финансовый аналитик. Пиши кратко и по-русски, без списков и без инвестиционных советов.",
    max_tokens=500,
)

# Если Claude не ответил, сводка всё равно уйдёт, просто без комментария
if comment is not None:
    text = text + "\n\nКомментарий:\n" + comment

# --- 8. Отправка ---
send_message(text)
print("Сообщение отправлено")