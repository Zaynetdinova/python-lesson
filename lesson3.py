# Урок 3: функции и JSON
import json

flats = [
    {"complex": "ЖК Цветы", "price": 5100000, "area": 42.5},
    {"complex": "ЖК Парк", "price": 3900000, "area": 31.0},
    {"complex": "ЖК Le Cristall", "price": 7000000, "area": 27.0},
    {"complex": "ЖК Premium", "price": 8000000, "area": 35.0},
    {"complex": "ЖК Life", "price": 3900000, "area": 30.0},
]


def price_per_m2(flat):
    return flat["price"] / flat["area"]


def find_cheaper(flats, limit):
    result = []
    for flat in flats:
        if flat["price"] < limit:
            result.append(flat)
    return result


def find_expensive(flats, limit):
    result = []
    for flat in flats:
        if flat["price"] > limit:
            result.append(flat)
    return result


# 1. Цена за м² через функцию
for flat in flats:
    print(f"{flat['complex']}: {price_per_m2(flat):.0f} ₽/м²")

# 2. Квартиры дешевле 4 млн
for flat in find_cheaper(flats, 4000000):
    print(f"Дешевле 4 млн: {flat['complex']}, {flat['price']} ₽")

# 3. Квартиры дороже 3,9 млн
for flat in find_expensive(flats, 3900000):
    print(f"Дороже 3,9 млн: {flat['complex']}, {flat['price']} ₽")

# 4. Запись в файл
with open("flats.json", "w", encoding="utf-8") as f:
    json.dump(flats, f, ensure_ascii=False, indent=2)

# 5. Чтение из файла
with open("flats.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)

for flat in loaded:
    print(flat["complex"])