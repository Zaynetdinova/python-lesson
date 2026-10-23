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
        if flat["price"] <= limit:
            result.append(flat)
    return result

cheap = find_cheaper(flats, 3900000)
for flat in cheap:
    print(f"Дешевле 4 млн: {flat['complex']}, {flat['price']} ₽")

def find_expensive(flats, limit):
    result = []
    for flat in flats:
        if flat["price"] > limit:
            result.append(flat)
    return result

expensive = find_expensive(flats, 3900000)
for flat in expensive:
    print(f"Дороже 3900000: {flat['complex']}, {flat['price']} ₽")
