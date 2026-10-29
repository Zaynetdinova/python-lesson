# Урок 10: классификатор заявок
#
# Что делает скрипт:
# 1. Читает входящие заявки из inbox.json
# 2. Пропускает те, что уже обработаны раньше (по id)
# 3. Просит Claude разобрать каждую заявку в JSON и проверяет ответ
# 4. Сохраняет результат в processed_leads.json
# 5. Присылает в Telegram сводку, срочные заявки и сообщения о неразобранных заявках
#
# Нужны: claude_utils.py, telegram_utils.py, inbox.json и в .env
# ANTHROPIC_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

import json
from pathlib import Path

import pandas as pd

from claude_utils import ask_claude
from telegram_utils import send_message
from classifier import SYSTEM, ALLOWED_CATEGORIES, ALLOWED_URGENCY, parse_json, validate_lead

INBOX_FILE = "inbox.json"
PROCESSED_FILE = "processed_leads.json"

def classify(item):
    """Разбирает одну заявку. Возвращает словарь или None."""
    raw = ask_claude(item["text"], system=SYSTEM, max_tokens=400)
    if raw is None:
        return None

    lead = parse_json(raw)
    if not validate_lead(lead):
        return None

    lead["id"] = item["id"]
    lead["source"] = item["source"]
    return lead


def load_json_list(path):
    """Читает список из JSON-файла. Если файла нет, возвращает пустой список."""
    if not Path(path).exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# --- 1. Читаем входящие и уже обработанные заявки ---
inbox = load_json_list(INBOX_FILE)
processed = load_json_list(PROCESSED_FILE)

# --- Пункт 4: защита от повторной обработки ---
# Множество (set) id, которые уже есть в processed_leads.json
processed_ids = {lead["id"] for lead in processed}

new_items = [item for item in inbox if item["id"] not in processed_ids]
print(f"Всего заявок: {len(inbox)}, уже обработано: {len(inbox) - len(new_items)}, новых: {len(new_items)}")

if not new_items:
    print("Новых заявок нет.")
    exit()

# --- 2. Разбираем новые заявки ---
new_leads = []
failed_ids = []

for item in new_items:
    lead = classify(item)

    if lead is None:
        # --- Пункт 5: сообщаем, что заявка не разобрана ---
        failed_ids.append(item["id"])
        print(f"Заявка #{item['id']} не разобрана")
        send_message(f"Заявка #{item['id']} не разобрана, проверь вручную.")
        continue

    new_leads.append(lead)

# --- 3. Сохраняем: старые + новые разобранные ---
# Неразобранные заявки в файл НЕ попадают, поэтому при следующем запуске
# скрипт попробует разобрать их снова.
processed.extend(new_leads)

with open(PROCESSED_FILE, "w", encoding="utf-8") as f:
    json.dump(processed, f, ensure_ascii=False, indent=2)

if not new_leads:
    print("Ни одну новую заявку разобрать не удалось.")
    exit()

# --- 4. Сводка по новым заявкам (pandas) ---
df = pd.DataFrame(new_leads)
real = df[df["category"] != "spam"]

summary = [
    f"Новых заявок: {len(df)} (спам: {len(df) - len(real)}, не разобрано: {len(failed_ids)})",
    "",
    "По категориям:",
]
for category, count in real["category"].value_counts().items():
    summary.append(f"  {category}: {count}")

summary.append("")
summary.append(f"Срочных: {(real['urgency'] == 'high').sum()}")
if real["budget"].notna().any():
    summary.append(f"Средний бюджет: {real['budget'].mean():,.0f} ₽".replace(",", " "))

send_message("\n".join(summary))

# --- 5. Срочные заявки отдельными сообщениями ---
for _, lead in real[real["urgency"] == "high"].iterrows():
    send_message(f"Срочная заявка #{lead['id']}: {lead['summary']}")

print("Готово")