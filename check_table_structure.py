import sqlite3

DB_PATH = "dog_nutrition.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(ingredient_wide);")
columns = cursor.fetchall()

print("Columns in ingredient_wide table:")
for col in columns:
    print(f"{col[1]} - {col[2]}")  # col[1] = column name, col[2] = data type

conn.close()
