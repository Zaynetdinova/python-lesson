# Урок 9: структурированный JSON-ответ и tool use

# Часть A: Claude достаёт данные клиента из текста сообщения и возвращает JSON
# Нужен файл claude_utils.py с функцией ask_claude и клиентом client
# и ANTHROPIC_API_KEY в .env

import json

from claude_utils import ask_claude

SYSTEM = (
    "Ты извлекаешь данные из сообщений клиентов агентства недвижимости. "
    "Студия это rooms = 0. Бюджет «до 6 млн» это 6000000. "
    'Пример: «Я Иван, ищу двушку за 8 млн срочно» → {"name": "Иван", "budget": 8000000, "rooms": 2, "urgency": "high"}'
    "Отвечай ТОЛЬКО валидным JSON без пояснений и без markdown. "
    'Формат: {"name": строка или null, "budget": число в рублях или null, '
    '"rooms": число или null, "urgency": "low" | "medium" | "high"}'
)

def extract_lead(message_text):
    """Достаёт данные клиента из сообщения. Возвращает словарь или None."""
    raw = ask_claude(message_text, system=SYSTEM, max_tokens=300)
    if raw is None:
        return None
 
    # Модель иногда оборачивает JSON в ```json ... ```, убираем обёртку
    cleaned = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
 
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        print("Claude вернул не JSON:", raw)
        return None


messages_list = [
    "Здравствуйте, я Анна. Ищу однушку до 6 млн, нужно срочно, до конца месяца.",
    "Добрый день! Интересует двухкомнатная квартира в новостройке, бюджет пока не определила.",
    "Меня зовут Тимур, смотрю студии для сдачи в аренду, до 4,5 млн, не спешу.",
]

leads = []
for text in messages_list:
    lead = extract_lead(text)
    if lead is None:
        continue
    leads.append(lead)
    print(lead)

with open("leads.json", "w", encoding="utf-8") as f:
    json.dump(leads, f, ensure_ascii=False, indent=2)


