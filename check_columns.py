import sqlite3

conn = sqlite3.connect("dog_nutrition.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(ingredients);")
columns = cursor.fetchall()
print("Number of columns:", len(columns))
for col in columns:
    print(col[1])  # prints column names

conn.close()
