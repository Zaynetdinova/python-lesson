# Урок 2: списки, словари, циклы

# --- Теория: список ---
prices = [4500000, 5100000, 3900000]
print(prices[0])
prices.append(6200000)
print(len(prices))

# --- Теория: словарь ---
flat = {"complex": "ЖК Цветы", "price": 5100000, "area": 42.5}
print(flat["price"])
flat["rooms"] = 1

# --- Теория: цикл for ---
for p in prices:
    print(f"Цена: {p} ₽")


# --- Задача: список квартир ---
flats = [
    {"complex": "ЖК Цветы", "price": 5100000, "area": 42.5},
    {"complex": "ЖК Парк", "price": 3900000, "area": 31.0},
    {"complex": "ЖК Le Cristall", "price": 7000000, "area": 27.0},
    {"complex": "ЖК Premium", "price": 8000000, "area": 35.0},
    {"complex": "ЖК Life", "price": 3900000, "area": 30.0},
]

# 1. Квартиры дешевле 5 млн
print("Квартиры дешевле 5 млн:")
for flat in flats:
    if flat["price"] < 5000000:
        print(f"{flat['complex']}: {flat['price']} ₽")

# 2. Цена за м² для каждой квартиры
print("Цена за м²:")
for flat in flats:
    price_per_m2 = flat["price"] / flat["area"]
    print(f"{flat['complex']}: {price_per_m2:.0f} ₽/м²")

# 3. Самая дорогая квартира
max_flat = flats[0]

for flat in flats:
    if flat["price"] > max_flat["price"]:
        max_flat = flat

print(f"Самая дорогая: {max_flat['complex']}, {max_flat['price']} ₽")

# 4. Самая дешёвая квартира (тот же приём, другой знак)
min_flat = flats[0]

for flat in flats:
    if flat["price"] < min_flat["price"]:
        min_flat = flat

print(f"Самая дешёвая: {min_flat['complex']}, {min_flat['price']} ₽")