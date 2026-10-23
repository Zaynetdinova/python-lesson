# Урок 6: pandas
# Данные: flats.json (создаётся скриптом make_flats.py)
import pandas as pd

# --- Теория: читаем JSON в таблицу ---
df = pd.read_json("flats.json")

print(df)                 # вся таблица
print(df.head(3))         # первые 3 строки
print(df.shape)           # (строк, столбцов)
print(df.columns)         # названия столбцов
df.info()                 # типы данных и пропуски

# --- Теория: статистика по столбцу ---
print(df["price"].mean())       # средняя цена
print(df["price"].max())        # максимум
print(df["price"].min())        # минимум
print(df["price"].describe())   # сводка сразу

# --- Новый столбец: цена за м² ---
df["price_per_m2"] = (df["price"] / df["area"]).round(0)
print(df)

# --- Фильтры ---
# одно условие
cheap = df[df["price"] < 5000000]
print(cheap)

# несколько условий (скобки обязательны, & значит "и", | значит "или")
good = df[(df["price"] < 6000000) & (df["area"] > 30)]
print(good)

# --- Сортировка ---
df_sorted = df.sort_values("price_per_m2", ascending=False)
print(df_sorted[["complex", "price_per_m2"]])

# по нескольким столбцам: сначала комнаты (по возрастанию),
# внутри комнатности цена за м² (по убыванию)
print(df.sort_values(["rooms", "price_per_m2"], ascending=[True, False]))


# --- Домашнее задание 6 ---

# 1. Данные дополнены полями rooms и district (см. make_flats.py)

# 2. Средние значения
print(f"Средняя цена: {df['price'].mean():.0f} ₽")
print(f"Средняя цена за м²: {df['price_per_m2'].mean():.0f} ₽")
print(f"Средняя площадь: {df['area'].mean():.1f} м²")

# 3. Группировка
print("Средняя цена за м² по числу комнат:")
print(df.groupby("rooms")["price_per_m2"].mean().round(0))

print("Средняя цена за м² по районам:")
print(df.groupby("district")["price_per_m2"].mean().round(0))

# несколько показателей сразу (count показывает, сколько квартир в группе)
print(df.groupby("district")["price_per_m2"].agg(["mean", "min", "max", "count"]))

# 4. Три самые дешёвые квартиры по цене за м²
print("Три самые дешёвые по цене за м²:")
print(df.nsmallest(3, "price_per_m2")[["complex", "district", "price_per_m2"]])

# 5. Квартиры до 6 млн, отсортированные по цене за м², сохраняем в CSV
under_6m = df[df["price"] < 6000000]
report = under_6m.sort_values("price_per_m2")
print(report[["complex", "price_per_m2"]])
report.to_csv("flats_report.csv", index=False, encoding="utf-8-sig")