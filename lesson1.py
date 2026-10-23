# Урок 1: переменные, f-строки, ввод данных, условия

# --- Теория: переменные и типы ---
name = "Ильмира"        # str, строка
age = 27                # int, целое число
price = 4500000.50      # float, дробное число
is_available = True     # bool, True/False

print(name)
print(type(age))

# --- Теория: f-строки ---
area = 42.5
total = 5100000
price_per_m2 = total / area

print(f"Квартира {area} м², цена {total} ₽")
print(f"Цена за м²: {price_per_m2:.0f} ₽")

# --- Теория: арифметика ---
print(10 + 3)    # 13
print(10 - 3)    # 7
print(10 * 3)    # 30
print(10 / 3)    # 3.333...
print(10 // 3)   # 3
print(10 % 3)    # 1
print(2 ** 5)    # 32


# --- Задача 1. Визитка ---
name = "Ильмира"
city = "Уфа"
purpose = "устроиться AI-автоматизатором"

print(f"Меня зовут {name}, живу в городе {city}, моя цель: {purpose}")


# --- Задача 2. Цена за м² ---
price = int(input("Цена квартиры в рублях: "))
area = float(input("Площадь в м²: "))

price_per_m2 = price / area
print(f"Цена за м²: {price_per_m2:.0f} ₽")


# --- Задача 3. Ипотечный пре-чек ---
price = int(input("Стоимость квартиры: "))
down_payment = int(input("Первоначальный взнос: "))

min_down_payment = price * 0.2

if down_payment < min_down_payment:
    print("Нужен больший первый взнос")
else:
    loan = price - down_payment
    print(f"Сумма кредита: {loan} ₽")