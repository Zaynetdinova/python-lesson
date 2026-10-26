import os

import anthropic
from dotenv import load_dotenv

load_dotenv()

if os.getenv("ANTHROPIC_API_KEY") is None:
    print("ANTHROPIC_API_KEY не найден в .env")
    exit()

client = anthropic.Anthropic()    # сам берёт ключ из переменной окружения

def ask_claude(prompt, system=None, max_tokens=300):
    """Отправляет запрос Claude и возвращает текст ответа или None при ошибке."""
    params = {
        "model": "claude-haiku-5-5",
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }
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
        print("Нет соединения с API.")
        return None
    except anthropic.APIStatusError as e:
        print(f"Ошибка API, код {e.status_code}")
        return None

    if message.stop_reason == "max_tokens":
        print("Внимание: ответ обрезан, увеличь max_tokens.")

    texts = [block.text for block in message.content if block.type == "text"]

    if not texts:
        print("В ответе нет текста (возможно, max_tokens слишком мал).")
        return None

    return "".join(texts)

answer = ask_claude("Объясни в двух предложениях, что такое API.")
print(answer)

answer = ask_claude(
    "Доллар вырос на 1.5% за день. Объясни в 2-3 предложениях, что это может значить.",
    system="Ты финансовый аналитик. Пиши кратко и по-русски, без списков и без инвестиционных советов.",
    max_tokens=500,
)
if answer is not None:
    print(answer)