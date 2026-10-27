# Часть B: Claude просит вызвать наши функции (ипотека, цена за м²), а потом отвечает

# ЧАСТЬ B: tool use (Claude просит вызвать наши функции)
# =====================================================================
import json
from pathlib import Path
import anthropic
 
from claude_utils import client
 
# --- Наши функции: их выполняет НАШ код, а не Claude ---
def get_mortgage_payment(price, down_payment, years, rate_pct):
    """Ежемесячный аннуитетный платёж в рублях."""
    loan = price - down_payment
    monthly_rate = rate_pct / 100 / 12
    n = years * 12
    payment = loan * monthly_rate / (1 - (1 + monthly_rate) ** -n)
    return round(payment)
 
 
def get_price_per_m2(price, area):
    """Цена за квадратный метр в рублях."""
    return round(price / area)

def find_cheaper_flats(limit):
    """Квартиры из flats.json дешевле limit (в рублях). Возвращает список словарей."""
    # Путь строим от места, где лежит этот файл, чтобы работало из любой папки
    flats_path = Path(__file__).parent / "flats.json"
 
    try:
        with open(flats_path, "r", encoding="utf-8") as f:
            flats = json.load(f)
    except FileNotFoundError:
        return "Файл flats.json не найден (сначала запусти make_flats.py)."
 
    return [flat for flat in flats if flat["price"] < limit]
 
 
# Словарь «имя инструмента -> функция», чтобы не писать цепочку if
TOOL_FUNCTIONS = {
    "get_mortgage_payment": get_mortgage_payment,
    "get_price_per_m2": get_price_per_m2,
    "find_cheaper_flats": find_cheaper_flats,
}
 
# --- Описание инструментов для Claude ---
# По description Claude решает, когда и как вызывать функцию
tools = [
    {
        "name": "get_mortgage_payment",
        "description": "Считает ежемесячный аннуитетный платёж по ипотеке в рублях.",
        "input_schema": {
            "type": "object",
            "properties": {
                "price": {"type": "number", "description": "Стоимость квартиры в рублях"},
                "down_payment": {"type": "number", "description": "Первоначальный взнос в рублях"},
                "years": {"type": "integer", "description": "Срок кредита в годах"},
                "rate_pct": {"type": "number", "description": "Годовая ставка в процентах"},
            },
            "required": ["price", "down_payment", "years", "rate_pct"],
        },
    },
    {
        "name": "get_price_per_m2",
        "description": "Считает цену за квадратный метр квартиры в рублях.",
        "input_schema": {
            "type": "object",
            "properties": {
                "price": {"type": "number", "description": "Стоимость квартиры в рублях"},
                "area": {"type": "number", "description": "Площадь квартиры в м²"},
            },
            "required": ["price", "area"],
        },
    },
    {
        "name": "find_cheaper_flats",
        "description": (
            "Ищет в базе квартир (файл flats.json) все квартиры дешевле заданного лимита. "
            "Для каждой квартиры возвращает: complex (название ЖК), price (цена в рублях), "
            "area (площадь в м²), rooms (число комнат, 0 это студия), district (район)."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "limit": {"type": "number", "description": "Максимальная цена в рублях (строго меньше)"},
            },
            "required": ["limit"],
        },
    },
]
 
 
def ask_with_tools(question, max_steps=5):
    """Задаёт вопрос Claude с доступом к инструментам. Возвращает текст ответа или None."""
    messages = [{"role": "user", "content": question}]
 
    # Цикл нужен, потому что Claude может вызвать инструменты несколько раз подряд.
    # max_steps защищает от бесконечного цикла.
    for _ in range(max_steps):
        try:
            response = client.messages.create(
                model="claude-haiku-5-5",
                max_tokens=1000,
                tools=tools,
                messages=messages,
            )
        except anthropic.APIError as e:
            print(f"Ошибка API Claude: {type(e).__name__}")
            return None
 
        # Если Claude не просит инструмент, ответ готов
        if response.stop_reason != "tool_use":
            texts = [block.text for block in response.content if block.type == "text"]
            return "".join(texts) if texts else None
 
        # Сохраняем ответ Claude (с запросами на вызов) в историю
        messages.append({"role": "assistant", "content": response.content})
 
        # Выполняем все запрошенные функции
        tool_results = []
        for block in response.content:
            if block.type != "tool_use":
                continue
 
            print(f"Claude просит вызвать: {block.name} {block.input}")
            func = TOOL_FUNCTIONS.get(block.name)
 
            if func is None:
                result = "Неизвестный инструмент"
            else:
                try:
                    result = func(**block.input)
                except (TypeError, ZeroDivisionError) as e:
                    result = f"Ошибка при вызове: {e}"
 
            # tool_use_id связывает результат с конкретным запросом
            tool_results.append(
                {"type": "tool_result", "tool_use_id": block.id, "content": str(result)}
            )
 
        # Результаты возвращаем Claude как сообщение пользователя
        messages.append({"role": "user", "content": tool_results})
 
    print("Слишком много шагов, остановились.")
    return None
 
 
# --- Проверка ---
# Платёж для этих данных должен быть около 34 400 ₽ (проверь вручную)
answer = ask_with_tools(
    "Квартира стоит 6 млн, площадь 42 м², взнос 1,2 млн, срок 20 лет, ставка 6%. "
    "Какая цена за м² и какой ежемесячный платёж?"
    "Что такое аннуитет?"
)

answer = ask_with_tools(
    "Какие у нас есть квартиры дешевле 5 млн рублей? Перечисли ЖК, район и цену, "
    "а в конце скажи, какая из них самая выгодная по цене за м²."
)

answer = ask_with_tools(
    "Что такое студия?"
)
print(answer)